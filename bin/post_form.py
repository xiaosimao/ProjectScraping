import web
import db_process
import time
import datetime
import os
import db_process as db
import sendEmail_v1 as sendEmail
import modelgenerateHtml_development as htmlgen
from multiprocessing import Process
#import modelgenerateHtml_development as htmlgen
#This file is to get input information from users,including their name, email
#address, the car they would like to receive information about.(car make,model,
#year of make)

#process 1
def click_mail_process(email,make,model,startyear,endyear,minPrice,maxPrice,time):
    html=htmlgen.generateHTML(make,model,startyear,endyear,minPrice,maxPrice,time)
    print email
    print html
    sendEmail.sendgridEmail(html,email)
#process 2
def mail_process():
    while(1):
        #read DB records
        rows = db.readDB()
        for row in rows:
            make=row[1]
            model=row[2]
            email=row[3]
            startyear=row[4]
            endyear=row[5]
            minPrice=row[6]
            maxPrice=row[7]
            time=row[8]
            html=htmlgen.generateHTML(make,model,startyear,endyear,minPrice,maxPrice,time)
            print email
            print html
            schedule.every().day.at("21:23").do(sendgridEmail(html, email))
            schedule.run_pending()
        time.sleep(62)
    
    
    
urls = (
  '/', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/',base="layout")

class Index(object):
    def GET(self):
        return render.subscribe_form()

    def POST(self):
        tempcurrentTime=time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
        form = web.input(username="Nobody", make="Toyota", model="Camry", email="test@ncsu.edu", minYear="2007", maxYear="2015", minPrice="500", maxPrice="100000", currentTime=tempcurrentTime)        
        #xmlprocess.writeXml("bin/users.xml",form.make,form.model,form.year,form.username,tempcurrentTime,form.email)
        db_process.writeDB(form.username, form.make, form.model, form.email, form.minYear, form.maxYear, form.minPrice, form.maxPrice, form.currentTime)
        p = Process(target=click_mail_process, args=(form.email,form.make,form.model,form.minYear,form.maxYear,int(form.minPrice),int(form.maxPrice),(datetime.datetime.now()-datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")))
        p.start()
        greeting = "%s, %s, %s, %s, %s, %s, %s, %s \n Please wait for ProjectScraping Email" % (form.username, form.make, form.model, form.email, form.minYear, form.maxYear, form.minPrice, form.maxPrice)
        return render.index(greeting = greeting)

if __name__ == "__main__":
    Process(target=mail_process).run()
    app.run()


