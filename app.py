import json

from flask import Flask, redirect
from flask import render_template, request
from stellar_base.builder import Builder
from stellar_base.keypair import Keypair

"""
    # Find whether an account sent money
    http://horizon-testnet.stellar.org/accounts/GAFNKWN2GX7FCCSYLS36OUN2NIWJAU4UVZC44MVTQQX6HDAUZ2UUQL6I/transactions
"""
app = Flask(__name__)


def send_payment(amount, item, asset='XLM'):
    flag = False
    try:
        # builder = Builder(secret=MEMBER_SEED)
        builder = Builder(secret=MEMBER_SEED)
        builder.append_payment_op(SITE_ADDR, amount, asset)
        builder.add_text_memo(item)
        builder.sign()
        s = builder.submit()
        print(s)
        flag = True
    except Exception as ex:
        print('Error in Payment')
        print(str(ex))
    finally:
        return flag


@app.route("/gen_address")
def gen_address():
    kp = Keypair.random()
    publickey = kp.address().decode()
    seed = kp.seed().decode()
    return json.dumps({'publickey': publickey, 'seed': seed})


@app.route("/thanks")
def thanks():
    return 'Thanks for your order'


@app.route("/pay", methods=['GET', 'POST'])
def pay():
    result = False
    item = 'Buyer - Jon Doe'

    amt = 10
    result = send_payment(amt, item)
    if result:
        return redirect("/thanks", code=302)
    else:
        return 'Invalid Transaction'


@app.route("/basket")
def basket():
    return render_template('basket.html')


@app.route("/checkout")
def checkout():
    return render_template('checkout.html')


@app.route("/")
def main():
    # k, s = gen_address()
    # print(k)
    # print(s)
    return render_template('home.html')


if __name__ == "__main__":
    # SITE_ADDR = 'GA36WRQJSJIKTAKD2MJNVGUXUGLBAXEKKXIQENRNU3J5PNEZLCCD3M5L'
    # SITE_SEED = 'SABA7LBKQOIWZENE7TU442ZLJM7HAPRKTFBSM656UONB2UMCVB3MDK24'
    #
    # MEMBER_ADD = 'GBYVSIXRDKJDHY5JGK6N37RFLZ2JDH3GDZPYOWXITQCWOCQ26VSRSXZF'
    # MEMBER_SEED = 'SBGUJJV6FSUL5S3AWH36XPYFIGGMAV3RQK7NSZWO7PTIS2ZCSPFVREGT'

    SITE_ADDR = 'GAFNKWN2GX7FCCSYLS36OUN2NIWJAU4UVZC44MVTQQX6HDAUZ2UUQL6I'
    SITE_SEED = 'SCC2V25EPMDLWUXNOJNLTBFXMWDHLLNJOY4DN5LWIEKFMYADNPW2OFXX'

    MEMBER_ADD = 'GBYVSIXRDKJDHY5JGK6N37RFLZ2JDH3GDZPYOWXITQCWOCQ26VSRSXZF'
    MEMBER_SEED = 'SBGUJJV6FSUL5S3AWH36XPYFIGGMAV3RQK7NSZWO7PTIS2ZCSPFVREGT'

    app.run(debug=True)
