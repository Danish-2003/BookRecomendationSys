from flask import Flask,render_template,request
import pickle
import numpy as np


popular_df = pickle.load(open('data/popular01.pkl','rb'))
pt = pickle.load(open('data/pt (1).pkl','rb'))
books = pickle.load(open('data/books (1).pkl','rb'))
similarity_score = pickle.load(open('data/similarity_score.pkl','rb'))

app = Flask(__name__)


sampled_book = popular_df.sample(n=12)
@app.route('/')
def home():
    sampled_book = popular_df.sample(n=12)
    return render_template('/index.html',books=sampled_book )



@app.route('/book_page')
def book_home():
    return render_template('book_page.html',books=popular_df)


@app.route('/recommend')
def book_recommend():
    return render_template('recommend.html')



@app.route('/recommend_books',methods=['POST'])
def recommend():
    
    user_input = request.form.get('user_input')
    
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        item.extend(list(temp_df.drop_duplicates('title')['image'].values))

        data.append(item)

    print(data)
    # return render_template('recommend.html')
    return render_template('recommend.html',data=data)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run(debug=True)