from flask import Flask, render_template, request
import pygal
import numpy as np
import psycopg2
#import helper functions
from forms import make_cancer, make_state, make_race, make_compound, make_crop
from sqlgenerator import make_sql
from bokeh.layouts import gridplot
from bokeh.models import Plot, LinearAxis, Range1d,ColumnDataSource, FactorRange, CategoricalAxis, HoverTool, CategoricalScale, LinearColorMapper
from bokeh.models.glyphs import Text, Rect
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.util.browser import view

from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import file_html

from bokeh.transform import linear_cmap
from bokeh.embed import components
import time
from scipy.stats.stats import pearsonr

########################################################################################################################################

app = Flask(__name__)

#declare local postgres
conn_string = "host='localhost' dbname='project' user='hunterkelley' password='secret'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()
#declare dropdown lists
states = make_state()
cancers = make_cancer()
races = make_race()
compounds = make_compound()
crops = make_crop()

# Set "homepage" to welcome.html
@app.route('/')
def hello():
    return render_template("welcome.html")

########################################################################################################################################


#healthcare 1-d information
@app.route('/cancer',methods=['GET', 'POST'])
def cancer():
    if request.method == 'POST':
        cancer_info = str(request.form.get('cancer_info'))
        state_info = str(request.form.get('state_info'))
        if(state_info == ""): state_info = "All States"
        start_time = time.time()

        cur.execute(make_sql(str(request.form.get("event_info")),request.form))

        query_time = str(round((time.time() - start_time),5))
        r = cur.fetchall()
        rlist = list(r)
        #check metric toggle, Rate or Absolute
        if len(rlist) != 0:
            if (len(rlist[0]) == 2): #Absolute
                x, y = [], []
                for i in rlist:
                    x.append(i[0])
                    y.append(i[1])
            if (len(rlist[0]) == 3): #Rate
                x, y = [], []
                for i in rlist:
                    x.append(i[0])
                    y.append(i[1]/i[2])

        # line_chart = pygal.Line()
        # line_chart.title = 'Cancer Rate by Count'
        # line_chart.x_labels = map(str, range(x[0], x[-1]+1))
        # line_chart.add('Cancer', y)
        # graph_url = line_chart.render_data_uri()
        print(x)
        print(y)
        graph = figure(plot_width=650, plot_height=400, title=cancer_info + " Incidents in " + state_info + " Over Time")
        graph.line(x, y, color='red', line_width=4)
        script, div = components(graph)
        return render_template("cancer_results.html", div=div, script=script, query_time = query_time)
    elif request.method == 'GET':
        return render_template("cancer.html", states=states, races=races, cancers=cancers)

######################################################################################################################################################


@app.route('/pesticides',methods=['GET', 'POST'])
def pesticides():
    if request.method == 'POST':
        print("Request is: ", request.form)
        compound_info = str(request.form.get('compound_info'))
        # chart_type = str(request.form.get('chart_type'))
        start_time = time.time()
        cur.execute(make_sql("Pesticides", request.form))
        query_time = str(round((time.time() - start_time),5))
        r = cur.fetchall()
        rlist = list(r)
        years, pesticides = [], []
        for i in rlist:
            print(i)
            years.append(i[0]) ##years
            pesticides.append(i[1]) ##pesticides
        
        graph = figure(plot_width=650, plot_height=400,title = compound_info + "Over Time", x_axis_label = 'Year', y_axis_label = 'Units (kg)')
            
        # if(chart_type == "Line"):
        graph.line(years, pesticides, color='blue', line_width=4)
        script, div = components(graph)

        # elif(chart_type == "Histogram"):
        #     print("Years is: ", years)
        #     print("Prices are: ", pesticides)
        #     graph.vbar(x = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], width=0.3, top=pesticides)
        #     #graph.xgrid.grid_line_color = None
        #     #graph.y_range.start = 0
        #     script, div = components(graph)

        return render_template("pesticides_results.html", script = script, div = div, query_time = query_time)

    elif request.method == 'GET':
        return render_template("pesticides.html", states=states, compounds=compounds, crops=crops)



########################################################################################################################################

@app.route('/economic', methods=['GET', 'POST'])
def economic():
    if request.method == 'POST':
        #Inputs from request form: 'chart_type', 'company_sector', 'company_sector2'
        print("Request form is: ", request.form)
        chart_type = str(request.form.get('chart_type'))
        company_sector = str(request.form.get('company_sector'))
        company_sector2 = str(request.form.get('company_sector2'))

        if(company_sector == "S&P500"): company_sector = "sp500"
        elif(company_sector == "Healthcare Sector"): company_sector = "healthcare"
        elif(company_sector == "Specialty Chemicals"): company_sector = "specialtychems"
        elif(company_sector == "Monsanto"): company_sector = "monsanto"

    

        if company_sector2 == "--":

            start_time = time.time()
            cur.execute("SELECT year, price FROM "+ company_sector+ " WHERE year > 2000 ORDER BY year ASC;")
            query_time = str(round((time.time() - start_time),5))
            r = cur.fetchall()
            rlist = list(r)
            years, company_sector_price = [], []

            for i in rlist:
                years.append(i[0])
                company_sector_price.append(i[1])

            graph = figure(plot_width=650, plot_height=400,title = str(request.form.get('company_sector')) + "Over Time", x_axis_label = 'Year', y_axis_label = 'Price')
            
            if(chart_type == "Line"):
                graph.line(years, company_sector_price, color='blue', line_width=4)
                script, div = components(graph)

            elif(chart_type == "Histogram"):
                graph.vbar(x = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], width=0.3, top=company_sector_price)
                #graph.xgrid.grid_line_color = None
                #graph.y_range.start = 0
                script, div = components(graph)

            return render_template("economic_results.html", script = script, div = div, query_time = query_time)

        elif company_sector2 != "--":
            if(company_sector2 == "S&P500"): company_sector2 = "sp500"
            elif(company_sector2 == "Healthcare Sector"): company_sector2 = "healthcare"
            elif(company_sector2 == "Specialty Chemicals"): company_sector2 = "specialtychems"
            elif(company_sector2 == "Monsanto"): company_sector2 = "monsanto"

            start_time = time.time()
            cur.execute("SELECT " + company_sector +".year, " + company_sector + ".price, " + company_sector2 + ".price FROM " + company_sector + " INNER JOIN " + company_sector2 + " ON " + company_sector +".year = " + company_sector2 + ".year;")
            query_time = str(round((time.time() - start_time),5))
            r = cur.fetchall()
            rlist = list(r)
            years, company_sector_price, company_sector2_price = [], [], []
            for i in rlist:
                years.append(i[0])
                company_sector_price.append(i[1])
                company_sector2_price.append(i[2])

            graph = figure(plot_width=650, plot_height=400,title = str(request.form.get('company_sector')) + " Performance Over Time", x_axis_label = 'Year', y_axis_label = 'Price')
            if(chart_type == "Line"):
                graph.line(years, company_sector_price, color='blue', line_width=4)
                script, div = components(graph)

            elif(chart_type == "Histogram"):
                graph.vbar(x = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], width=0.3, top=company_sector_price)
                #graph.xgrid.grid_line_color = None
                #graph.y_range.start = 0
                script, div = components(graph)

            np_comp1 = np.array(company_sector_price)
            np_comp2 = np.array(company_sector2_price)
            np_ratio = np_comp1/np_comp2

            graph2 = figure(plot_width=650, plot_height=400,title = str(request.form.get('company_sector')) + " v.s. " + str(request.form.get('company_sector2')), x_axis_label = 'Year', y_axis_label = 'Price Ratio')
            # Setting the second y axis range name and range
            graph2.extra_y_ranges = {"Ratio": Range1d(start= min(np_ratio), end=max(np_ratio))}   
            # Adding the second axis to the plot.  
            # graph2.add_layout(LinearAxis(y_range_name="Ratio"), 'right') 
            graph2.line(years, np_ratio, color='red', line_width=4)
            script2, div2 = components(graph2)

            return render_template("economic_results.html", script = script, div = div, script2 = script2, div2 = div2, query_time=query_time)


    elif request.method == 'GET':
        return render_template("economic.html")


########################################################################################################################################

#([('chart_type', 'Line'), ('event_type', 'Incidence'), ('metric_info', 'Rate'), ('sex_info', ''), ('state_info', 'Alabama'), ('race_info', 'Black'), ('cancer_info', 'Brain and Other Nervous System'), ('compound_info', '2,4-D'), ('crop_info', 'corn'), ('submit form', '')])

@app.route('/pesticides_cancer', methods=['GET', 'POST'])
def pesticide_cancer():
    if request.method == 'POST':
        state_info = str(request.form.get('state_info'))
        start_time = time.time()
        cur.execute(make_sql("PesticidesCancer", request.form))
        query_time = str(round((time.time() - start_time),5))
        r = cur.fetchall()
        rlist = list(r)
        ys, xs = [], []
        for i in rlist: 
            ys.append(i[1])
            xs.append(i[3])
        rsquared = pearsonr(xs, ys)[0]
        print("RSQUARED IS: ", rsquared)
        graph = figure(plot_width=650, plot_height=400)
        graph.scatter(xs, ys, marker="square")
        script, div = components(graph)

        return render_template("pesticides_cancer_results.html", script=script, div=div, query_time=query_time, rsquared=rsquared)
    elif request.method == 'GET':
        return render_template("pesticides_cancer.html", states=states, compounds=compounds, crops=crops, races=races, cancers=cancers)

########################################################################################################################################

@app.route('/specialty', methods=['GET', 'POST'])
def specialty():
    if request.method == 'POST':
        this_state = str(request.form.get('state_info'))
        start_time = time.time()
        sql = "SELECT z.year, z.yearly_total FROM (SELECT o.year, o.state, o.yearly_total from (select j.year, j.state, yearly_total from (select sum(count) as yearly_total, state, year from Incidence where cancer_type = 'All Cancer Sites Combined' and sex = 'Male and Female' group by state, year) j inner join (select avg(total), i.state from (select sum(count) as total, state from Incidence where cancer_type = 'All Cancer Sites Combined' and sex = 'Male and Female' group by state, year) i group by i.state) av on j.yearly_total > av.avg and j.state = av.state order by j.state, year) o inner join (select state, year from pesticides where compound = 'GLYPHOSATE' and total > 500000) p on p.state = o.state and p.year = o.year) z where z.state = '" + this_state + "';"
        cur.execute(sql)
        r = cur.fetchall()
        ilist = list(r)
        yrs_high = []
        for i in ilist:
            yrs_high.append(i[0])

        #TODO Graph the years in which glyphosate and cancer rate were high for a given state

        this_race = str(request.form.get('race_info'))
        this_race2 = str(request.form.get('race_info2'))
        #sql = "select o.state, o.year, o.perc1, p.perc2 from (select year, state, CAST(sum(count) as decimal)/CAST(sum(population) as decimal) as perc1 from incidence where race = '" + this_race + "' and cancer_type = 'All Cancer Sites Combined' and sex = 'Male and Female' group by state, year order by state, year) o inner join (select year, state, CAST(sum(count) as decimal)/CAST(sum(population) as decimal) as perc2 from incidence where race = '" + this_race2 + "' and cancer_type = 'All Cancer Sites Combined' and sex = 'Male and Female' group by state, year order by state, year) p on o.state = p.state and o.year = p.year and perc2 > perc1"
        sql = "select u.year from (select o.state, o.year, o.perc1, p.perc2 from (select year, state, CAST(sum(count) as decimal)/CAST(sum(population) as decimal) as perc1 from incidence where race = '" + this_race + "' and cancer_type = 'All Cancer Sites Combined' and sex = 'Male and Female' group by state, year order by state, year) o inner join (select year, state, CAST(sum(count) as decimal)/CAST(sum(population) as decimal) as perc2 from incidence where race = '" + this_race2 + "' and cancer_type = 'All Cancer Sites Combined' and sex = 'Male and Female' group by state, year order by state, year) p on o.state = p.state and o.year = p.year and perc2 < perc1) u where u.state = '" + this_state + "';"
        cur.execute(sql)
        j = cur.fetchall()
        jlist = list(j)
        yrss = []
        for v in jlist:
            yrss.append(v[0])
        print(yrss)

        #TODO: Display the state and year in which the percentage of one race's cancer rate surpass the rate of another's

        sql = "select a.state, a.year, a.total, b.count from (select i.year, i.state, i.total from (select year, state, total from pesticides where compound = 'GLYPHOSATE') i inner join (select avg(total) as av, stddev(total) sdv, state from pesticides where compound = 'GLYPHOSATE' group by state) j on i.state = j.state and i.total > (j.av + j.sdv)) a inner join (select o.year, o.state, o.count from (select year, state, count from Incidence where sex = 'Male and Female' and cancer_type = 'All Cancer Sites Combined' and race = 'All Races') o inner join (select avg(count) as av, stddev(count) sdv, state from Incidence where sex = 'Male and Female' and cancer_type = 'All Cancer Sites Combined' and race = 'All Races' group by state) p on o.state = p.state and o.count < (p.av - p.sdv)) b on a.state = b.state and b.year = a.year order by a.state,a.year;"
        cur.execute(sql)
        query_time = str(round((time.time() - start_time),5))
        k = cur.fetchall()
        klist = list(k)
        tups_high_low = []
        for m in klist:
            tups_high_low.append((m[0], m[1]))
        print(query_time)

        #TODO: Display the state, year, total of pesticde used, and count of all cancer
        return render_template("specialty.html", states=states, races=races, yrs_high = yrs_high, tups_high_low=tups_high_low, yrss = yrss)
    elif request.method == 'GET':
        return render_template("specialty.html", states=states, races=races)

########################################################################################################################################


if __name__ == '__main__':
    app.run(debug=True)
    #app.run()