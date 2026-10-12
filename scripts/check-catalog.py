#!/usr/bin/env python3
"""Validate a secret-free, site-specific catalog. No network or payment writes."""
import argparse
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ['root must be an object']
    allowed = {'environment', 'site', 'products'}
    if set(data) - allowed:
        errors.append('unknown root fields; credentials do not belong in this file')
    if data.get('environment') not in ('test', 'prod'):
        errors.append('environment must be test or prod')
    if not isinstance(data.get('site'), str) or not data['site'].strip():
        errors.append('site must be a nonempty site identifier')
    products = data.get('products')
    if not isinstance(products, list) or not products:
        return errors + ['products must be a nonempty list']
    seen_skus, seen_ids = set(), set()
    for index, item in enumerate(products):
        label = f'products[{index}]'
        if not isinstance(item, dict):
            errors.append(f'{label}: must be an object')
            continue
        fields = {'sku', 'name', 'type', 'amount', 'currency', 'billing_period',
                  'entitlement', 'validity', 'refund_policy', 'platform_product_id'}
        if set(item) - fields:
            errors.append(f'{label}: unknown fields; keep secrets out of catalogs')
        for field in ('sku', 'name', 'entitlement', 'validity', 'refund_policy'):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f'{label}: {field} must be a nonempty string')
        sku = item.get('sku')
        if isinstance(sku, str):
            if sku in seen_skus:
                errors.append(f'{label}: duplicate sku')
            seen_skus.add(sku)
        kind = item.get('type')
        if kind not in ('one_time', 'subscription'):
            errors.append(f'{label}: type must be one_time or subscription')
        period = item.get('billing_period')
        if kind == 'subscription' and (not isinstance(period, str) or not period.strip()):
            errors.append(f'{label}: subscription requires billing_period')
        if kind == 'one_time' and period is not None:
            errors.append(f'{label}: one_time cannot have billing_period')
        amount = item.get('amount')
        try:
            if not isinstance(amount, str) or not re.fullmatch(r'\d+(?:\.\d+)?', amount):
                raise ValueError()
            parsed = Decimal(amount)
            if not parsed.is_finite() or parsed <= 0:
                raise ValueError()
        except (InvalidOperation, ValueError):
            errors.append(f'{label}: amount must be a positive decimal string')
        currency = item.get('currency')
        if not isinstance(currency, str) or not re.fullmatch(r'[A-Z]{3}', currency):
            errors.append(f'{label}: currency must be an uppercase three-letter code')
        product_id = item.get('platform_product_id')
        if product_id is not None:
            if not isinstance(product_id, str) or not product_id.strip():
                errors.append(f'{label}: platform_product_id must be a nonempty string')
            elif product_id in seen_ids:
                errors.append(f'{label}: duplicate platform_product_id')
            else:
                seen_ids.add(product_id)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog='''
Schema: {"site":"site-slug","environment":"test" or "prod","products":[...]}
Each product: sku, name, type (one_time/subscription), amount (positive decimal
string), currency (uppercase ISO code), entitlement, validity, refund_policy.
Subscription also requires billing_period. platform_product_id is optional.
Use separate files for test/prod. Do not include credentials or customer data.
This tool checks shape and duplicates only; verify supported currencies, currency
precision, billing periods, tax rules, product ownership and approved prices
against official data separately. It never contacts Waffo or creates a payment.
''', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('catalog', type=Path)
    args = parser.parse_args()
    try:
        with args.catalog.open(encoding='utf-8') as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        parser.exit(2, 'Cannot read a valid UTF-8 JSON catalog; contents not printed.\n')
    errors = validate(data)
    if errors:
        for message in errors:
            print(message)
        return 1
    print(f'Catalog valid: {len(data["products"])} products. No API or payment verification performed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
