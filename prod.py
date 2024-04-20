from flask import Flask,request,render_template
import pickle

app = Flask(__name__)

products = pickle.load(open('products.pkl','rb'))
sim = pickle.load(open('cos_similarity.pkl','rb'))

prod_names = products['name'].values

def reccomend(new_product):
    ind = products[products['name'] == new_product].index[0]
    distance = sorted(list(enumerate(sim[ind])),reverse = True,key = lambda x: x[1])
    recommendations = []
    for i in distance[1:6]:
        recommendations.append(products['name'].iloc[i[0]])
        
    return recommendations
        
@app.route('/')
def homepage():
    return render_template('product.html',prod_names = prod_names)

@app.route('/recco',methods = ['POST'])
def do_recommendation():
    prod_title = request.form.get('prod')
    reccos = reccomend(prod_title)
    return render_template('product.html',reccos = reccos,prod_names = prod_names,prod_title = prod_title)


if __name__ == '__main__':
    app.run(debug=True)