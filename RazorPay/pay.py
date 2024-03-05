from flask import Flask, render_template,request
import razorpay

app = Flask(__name__)

key_id='rzp_test_0eGEDnUNnnWiGh'
key_secret='3wVjDIgFRBCDF2X6c2kqt91Z'
client=razorpay.Client(auth=(key_id,key_secret))



def check_out(amount):
    data={
        'amount':amount*100,
        'currency':"INR",
        'receipt':'Print Kiosk',
        'notes':{
            'name':"Print Kiosk",
            "Payment_for":"Print(s)"
            #name here can be the email of the user (this is completely optional)
        }
    }

    #server orderid
    order=client.order.create(data=data)
    id=order['id']
    return str(id)
    
    # print(order)

    

@app.route('/')
def index():
    pages=10
    amount=10*3 # Rps 3 per page
    id=check_out(amount)
    
    return render_template('payment.html', order_id=id)

@app.route('/verify', methods=['POST'])
def verifying():
    payment_data = request.json
    
    try:
        client.utility.verify_payment_signature(payment_data)
        print('\n **** Payment Successful ****\n')
    except Exception as e:
        print("\n **** Payment Failed ****\n",e)
    return 'Verification Done'
    

    
if __name__ == '__main__':
    app.run(debug=True)
