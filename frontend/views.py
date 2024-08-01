from flask import render_template, request, redirect, url_for


def login():
    return render_template('login.html')


def register():
    return render_template('register.html')


def logout():
    return render_template('login.html')
    

def index():
    return render_template('index.html')


def company_chart():
    company_name = request.args.get('company')
    share = request.args.get('share')
    return render_template('chart.html', company=company_name, share=share)


def compare_shares():
    company1_name = request.args.get('company1')
    company2_name = request.args.get('company2')
    if not company1_name or not company2_name:
        return redirect(url_for('index'))
    return render_template('compare_shares.html', company1=company1_name, company2=company2_name)



def preferences():
    return render_template('preferences.html')


def purchases():
    return render_template('purchases.html')
