import hashlib


def check_click_sign(params, secret_key):
    sign_string = "{}{}{}{}{}{}{}".format(
        params.get('click_trans_id'),
        params.get('service_id'),
        secret_key,
        params.get('merchant_trans_id'),
        params.get('amount'),
        params.get('action'),
        params.get('sign_time'),

    )

    return hashlib.md5(sign_string.encode('utf-8')).hexdigest()