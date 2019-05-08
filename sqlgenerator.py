def make_sql(page, aList):
	
	dimensions = 0
	for each in aList:
		if str(aList.get(each)) != "":
			dimensions += 1


	sql = ""

	# Join
	if page == "PesticidesCancer":
		sql += "SELECT * FROM (SELECT year, SUM(" + aList.get('crop_info') + ") FROM Pesticides WHERE state = '" + aList.get('state_info') + "' AND compound = '" + aList.get('compound_info') + "' GROUP BY year ORDER BY year ASC) as x JOIN  (SELECT year, SUM(count) FROM " + aList.get('event_type') + " WHERE state = '" + aList.get('state_info') + "' AND race = '" + aList.get('race_info') + "' AND sex = '" + aList.get('sex_info') + "' AND cancer_type = '" + aList.get('cancer_info') + "' GROUP BY year ORDER BY year ASC) as y ON x.year = y.year;"

	
	# Pesticides
	elif page == "Pesticides":
		if dimensions == 1:
			if str(aList.get('state_info')) != "":
				sql += "SELECT year, SUM(total) FROM Pesticides WHERE state = '" + aList.get('state_info') + "' GROUP BY year ORDER BY year ASC;"
			elif str(aList.get('compound_info')) != "":
				sql += "SELECT year, SUM(total) FROM Pesticides WHERE compound = '" + aList.get('compound_info') + "' GROUP BY year ORDER BY year ASC;"
			else:
				sql += "SELECT year, SUM(" + aList.get('crop_info') + ") FROM Pesticides GROUP BY year ORDER BY year ASC;"
		elif dimensions == 2:
			if str(aList.get('state_info')) == "":
				sql += "SELECT year, SUM(" + aList.get('crop_info') + ") FROM Pesticides WHERE compound = '" + aList.get('compound_info') + "' GROUP BY year ORDER BY year ASC;"
			elif str(aList.get('compound_info')) == "":
				sql += "SELECT year, SUM(" + aList.get('crop_info') + ") FROM Pesticides WHERE state = '" + aList.get('state_info') + "' GROUP BY year ORDER BY year ASC;"
			else:
				sql += "SELECT year, SUM(total) FROM Pesticides WHERE state = '" + aList.get('state_info') + "' AND compound = '" + aList.get('compound_info') + "' GROUP BY year ORDER BY year ASC;"
		elif dimensions == 3:
			sql += "SELECT year, SUM(" + aList.get('crop_info') + ") FROM Pesticides WHERE state = '" + aList.get('state_info') + "' AND compound = '" + aList.get('compound_info') + "' GROUP BY year ORDER BY year ASC;"
		else:
			sql += "SELECT year, SUM(total) FROM Pesticides GROUP BY year ORDER BY year ASC;"

	# Cancer
	else:
		state = ""
		race = " AND race = 'All Races'"
		sex = " AND sex = 'Male and Female'"
		cancer = " AND cancer_type = 'All Cancer Sites Combined'"

		if dimensions == 3:
			# STATE
			if str(aList.get('state_info')) != "":
				state = "state = '" + aList.get('state_info') + "'"
			# RACE
			elif str(aList.get('race_info')) != "":
				race = "race = '" + aList.get('race_info') + "'"
			# SEX
			elif str(aList.get('sex_info')) != "":
				race = "race = 'All Races'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
			# CANCER TYPE
			elif str(aList.get('cancer_info')) != "":
				race = "race = 'All Races'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"

		elif dimensions == 4:
			# STATE / RACE
			if str(aList.get('state_info')) != "" and str(aList.get('race_info')) != "":
				state = "state = '" + aList.get('state_info') + "'"
				race = " AND race = '" + aList.get('race_info') + "'"
			# STATE / SEX
			elif str(aList.get('state_info')) != "" and str(aList.get('sex_info')) != "":
				state = "state = '" + aList.get('state_info') + "'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
			# STATE / CANCER TYPE
			elif str(aList.get('state_info')) != "" and str(aList.get('cancer_info')) != "":
				state = "state = '" + aList.get('state_info') + "'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"
			# RACE / SEX
			elif str(aList.get('race_info')) != "" and str(aList.get('sex_info')) != "":
				race = "race = '" + aList.get('race_info') + "'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
			# RACE / CANCER TYPE
			elif str(aList.get('race_info')) != "" and str(aList.get('cancer_info')) != "":
				race = "race = '" + aList.get('race_info') + "'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"
			# SEX / CANCER TYPE
			elif str(aList.get('cancer_info')) != "" and str(aList.get('sex_info')) != "":
				race = "race = 'All Races'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"

		elif dimensions == 5:
			# STATE / RACE / SEX
			if str(aList.get('cancer_info')) == "":
				state = "state = '" + aList.get('state_info') + "'"
				race = " AND race = '" + aList.get('race_info') + "'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
			# STATE / SEX / CANCER TYPE
			elif str(aList.get('race_info')) == "":
				state = "state = '" + aList.get('state_info') + "'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"
			# STATE / RACE / CANCER TYPE
			elif str(aList.get('sex_info')) == "":
				state = "state = '" + aList.get('state_info') + "'"
				race = " AND race = '" + aList.get('race_info') + "'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"
			# RACE / SEX / CANCER TYPE
			elif str(aList.get('state_info')) == "":
				race = "race = '" + aList.get('race_info') + "'"
				sex = " AND sex = '" + aList.get('sex_info') + "'"
				cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"

		elif dimensions == 6:
			# STATE / RACE / SEX / CANCER TYPE
			state = "state = '" + aList.get('state_info') + "'"
			race = " AND race = '" + aList.get('race_info') + "'"
			sex = " AND sex = '" + aList.get('sex_info') + "'"
			cancer = " AND cancer_type = '" + aList.get('cancer_info') + "'"
			
		else:
			# TOTAL
			race = "race = 'All Races'"
			sex = " AND sex = 'Male and Female'"

		if(aList.get('metric_info') == 'Rate'):
			sql += "SELECT year, SUM(count), SUM(population) FROM " + page + " WHERE " + state + race + sex + cancer + " GROUP BY year ORDER BY year ASC;"
		else: #Absolute
			sql += "SELECT year, SUM(count) FROM " + page + " WHERE " + state + race + sex + cancer + " GROUP BY year ORDER BY year ASC;"

			
	print(sql)
	return sql