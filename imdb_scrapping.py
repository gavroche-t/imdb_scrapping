##First, import all needed libraries:

from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
from time import sleep
from random import randint

#The headers section defines the language. You can also expand it to define other functionalities. 
headers = {"Accept-Language": "en-US, en;q=0.5"}

#List has all the beginning movies of each page. IMDb, by default, has 50 itens per page.
list = [1, 51]
pages = [str(i) for i in list]
#Years_url has the initial and final year that the want to loop. 
years_url = [str(i) for i in range(2000, 2020)]

##Define the vectors used for appending the infos:

names_all = []
name_code_all = []
years_all = []
time_all = []
imdb_all = []
metascore_all = []
votes_all = []
revenue_all = []
ratings_all = []
conjunto_cod_all = []
conjunto_all = []
final_section_all = []
gender_dic_all = []
gender_actor_all = []
gender_dic1_all = []
place_birth_direc_all = []
place_birth_act_all = []
year_birth_direc_all = []
year_birth_act_all = []
dic_points_all = []
actor_points_all = []
actor_placement_all = []
country_mov_all = []
language_mov_all = []
budget_mov_all = []
gross_usa_all = []
gross_world_all = []
opening_week_us_can_all = []
genres_mov_all = []


##Create the first loop, with year:
for year_url in years_url:
    print('Present year:', year_url)
    #Define a counter to be used later.
    counter = 1
    #Create the second loop. For each year, there are more than one page. 
    for page in pages:
        #Define the url. The structure is as follows. A special string (f) is used to insert the infos defined before.
        url_print = f'''https://www.imdb.com/search/title?release_date={year_url}&sort=boxoffice_gross_us,desc&start={page}'''
        #Define the response got from the url. We use the headers previously defined.
        response = requests.get(url_print, headers = headers)
        print('Present page:', page)
        #Print the link for any checks needed.
        print(url_print)
        
        ##Pause the loop. We don't want to be seen as bots, neither overcharge the server.
        sleep(randint(2,5))
        print(response)
        
        ##Extract html: 
        soup = BS(response.text, 'lxml')
        
        #Movie containers finds all the 'boxes' (seen in IMDb) containing each movie.
        movie_containers = soup.find_all('div', class_="lister-item mode-advanced")
        
        #We want to go through each box in our box list.
        for container in movie_containers:
            
            #We only want movies, no series. Series don't have Metascore.
            if container.find('div', class_ = 'ratings-metascore') is not None:
                
                #Get the name and append it to the main name list.
                name = container.h3.a.text
                names_all.append(name)
                
                print(f'''We are in the movie {counter}, {name}''')
                
                #Now, we want to find the links to extract the url to director and actor infos. 
                #All these infos are inside the 'staff' list.
                #Staff only works because there is only one 'p' with null class in each container!
                staff = container.find_all('p', class_='')
                                
                ##Find primary director url.
                director = []
                #Staff1 gets the first element in staff and finds the first 'a' in the tree.
                staff1 = staff[0].a
                #Our url is contained in the href. 
                main_director_code=str(staff1['href'])
                
                #Define a variable a as empty list, for future comparison.
                #Find secondary director url (if existing). 
                #Although we get it, we don't use it.
                a = []
                
                #Create an if clause in case there's no url in IMDb.
                if  main_director_code != a:
                    
                    #The next_sibling clause finds the next html element in the same branch of the tree. 
                    #Staff5 is a temporary var.
                    staff5 = staff1.next_sibling
                    #When an coma is found, we want it to go to next sibling, so it gets the actual info.
                    if "," in str(staff5):
                        staff5 = staff5.next_sibling
                    else: staff5 = []
                    
                    if staff5 != a:
                        sec_direc = staff5['href']
                
                ##Find the primary actor url.
                #Create a new var, staff2, with the info we need.
                staff2 = staff[0].span.next_sibling
                
                #Define our list.
                main_actor_code= []
                
                #The url are after the "Stars" text.
                if 'Stars:' in str(staff2):
                    staff3 = staff2.next_sibling
                    main_actor_code = staff3['href']
                                    
                ##Find the secondary actor url.
                ##Reminder: a = []
                if main_actor_code != a: 
                    staff4 = staff3.next_sibling 
                    if "," in str(staff4):
                        staff4 = staff4.next_sibling
                    else: staff4 = []
                    
                    sec_actor = staff4['href']
                    
                ##Now, create a list with our main actor and director codes. We won't use the secondary ones.
                final_staff = [main_director_code, main_actor_code] #, sec_direc_code, sec_actor_code]
                
                #The boolean vars here are needed for a troubleshooting. 
                #If the actor and director have the same url (for some Eastwood movies, p.e.), 
                #it reads both of them in the same iteration. To solve this problem of double appending, 
                #this boolean logic was implemented. It is quite simple, though :).
                read_director = False
                read_actor = False
                
                #For each element in final staff (director and actor urls).
                for i in final_staff:
                    
                    if i != a:
                        #We access a new page in IMDb with the url extracted.
                        url = f'''https://www.imdb.com{i}'''
                        response1 = requests.get(url)
                        sleep(randint(2,5))
                        soup1 = BS(response1.text, 'lxml')
                        
                        #Director page:
                        if i == main_director_code and not read_director:
                            read_director = True
                            print('We are in the director page, ', i)
                            
                            #genral e general1 are some frames with specific infos. Check the IMDb page for details.
                            general = soup1.find_all('div', attrs={'id':'filmo-head-director'})
                            general1 = soup1. find_all('div', attrs={"id":"name-born-info"})

                            #Place of birth director:
                            try:
                                temp = general1[0].time.next_sibling
                                place_birth1 = temp.next_sibling.text
                                place_birth_direc = str(place_birth1)
                            #Don't remember what this temp was supposed to do.
                            except AttributeError:
                                temp = general1[0].a.text
                            except Exception:
                                place_birth_direc = 'null'
                            place_birth_direc_all.append(place_birth_direc)
                            print('Place of birth director:', place_birth_direc)

                            #Year of birth actor:
                            try:
                                year_birth1 = general1[0].time.text
                                year_birth_direc = year_birth1[-6:-1]
                            except Exception:
                                year_birth_direc = 'null'
                            year_birth_direc_all.append(year_birth_direc)
                            print('Year of birth director:', year_birth_direc)

                            #Number of points (movies directed)
                            dic_points = general[0].a.next_sibling
                            dic_points_all.append(dic_points)

                            #Gender info:
                            #To do so, as there is no specific info about the gender, 
                            #We analize the bio and infer based on text analysis.
                            try:    
                                bio_dic = soup1.find('div', class_="inline").text
                            except AttributeError:
                                bio_dic = 'null'

                            #First possibility: without caps.
                            if " she " in str(bio_dic):
                                if ' he ' not in str(bio_dic): 
                                    gender_dic1 = 'female'
                                else: gender_dic1 = 'not sure'

                            elif " he " in str(bio_dic):
                                if " she " not in str(bio_dic):
                                    gender_dic1 = 'male'
                                else: gender_dic1 = 'not sure'

                            elif " his " in str(bio_dic):
                                if " hers " not in str(bio_dic):
                                    gender_dic1 = 'male'
                                else: gender_dic1 = 'not sure'

                            elif " hers " in str(bio_dic):
                                if " his " not in str(bio_dic):
                                    gender_dic1 = 'female'
                                else: gender_dic1 = 'not sure'

                            elif " him " in str(bio_dic):
                                if " her " not in str(bio_dic):
                                    gender_dic1 = 'male'
                                else: gender_dic1 = 'not sure'

                            elif " her " in str(bio_dic):
                                if " him " not in str(bio_dic):
                                    gender_dic1 = 'female'
                                else: gender_dic1 = 'not sure'

                            else: gender_dic1 = 'not sure'
                            gender_dic1_all.append(gender_dic1)

                            #Second possibility: with caps.
                            if "She" in str(bio_dic):
                                if 'He' not in str(bio_dic): 
                                    gender_dic = 'female'
                                else: gender_dic = 'not sure'

                            elif "He" in str(bio_dic):
                                if "She" not in str(bio_dic):
                                    gender_dic = 'male'
                                else: gender_dic = 'not sure'

                            elif " His " in str(bio_dic):
                                if " Hers " not in str(bio_dic):
                                    gender_dic1 = 'male'
                                else: gender_dic1 = 'not sure'

                            elif " Hers " in str(bio_dic):
                                if " His " not in str(bio_dic):
                                    gender_dic1 = 'female'
                                else: gender_dic1 = 'not sure'

                            elif " Him " in str(bio_dic):
                                if " Her " not in str(bio_dic):
                                    gender_dic1 = 'male'
                                else: gender_dic1 = 'not sure'

                            elif " Her " in str(bio_dic):
                                if " Him " not in str(bio_dic):
                                    gender_dic1 = 'female'
                                else: gender_dic1 = 'not sure'

                            else: gender_dic = 'not sure'
                            print("Director's gender is: ", gender_dic)
                            gender_dic_all.append(gender_dic)
                            print("""Director page finished.
                            ---------------------

                            """)

                            
                        ##Now, for the actor scrapping:
                        if i == main_actor_code and not read_actor:
                            read_actor = True
                            print("We are in actor page, ", i)
                            
                            #general3 is another frame with infos.
                            general3 = soup1.find_all('div', attrs={"id":"name-born-info"})

                            #Place birth actor:
                            try:
                                temp1 = general3[0].time.next_sibling
                                place_birth2 = temp1.next_sibling.text
                                place_birth_act = str(place_birth2)
                                print("Place of birth actor:", place_birth_act)
                            except AttributeError:
                                general3 = soup1. find_all('div', attrs={"id":"name-born-info"})
                                temp1 = general3[0].a.text
                            except Exception: 
                                place_birth_act = 'null'
                            place_birth_act_all.append(place_birth_act)    

                            #Year of birth actor:
                            try:
                                year_birth2 = general3[0].time.text
                                year_birth_act = year_birth2[-6:-1]
                            except Exception:
                                year_birth_act = 'null'
                            year_birth_act_all.append(year_birth_act)
                            print("Year of birth actor: ", year_birth_act)

                            #Actor's ranking (according to IMDB).
                            meter_box = soup1.find_all('div', attrs={"id":"meterHeaderBox"})
                            actor_placement1 = meter_box[0].a.text
                            actor_placement = actor_placement1[-4:]
                            actor_placement_all.append(actor_placement)
                            print("Actor's ranking: ", actor_placement)


                            #Actor's gender info is a bit different from the director gender info.
                            #There's a difference in code between actor and actress.
                            #We use this difference to get the right gender right away.
                            try:
                                map_gender = soup1.find_all('div', attrs={"id":"name-job-categories"})
                                gender_while = map_gender[0].a
                            except Exception:
                                gen_act = "not sure"

                            try:
                                while "Act" not in str(gender_while):
                                    gender_while = gender_while.next_sibling
                                print("While is:", gender_while)
                                gen_act = gender_while.text.strip().lower()
                                print("Actor gender was:", gen_act)
                            except Exception:
                                gen_act = "not sure"
                                print("Actor's while error.")

                            #Gender extraction:
                            if gen_act == 'actor':
                                gender_actor = 'male'
                            if gen_act == 'actress':
                                gender_actor = 'female'
                            if gen_act == 'not sure':
                                gender_actor = 'not sure'
                            gender_actor_all.append(gender_actor)
                            print('The actor gender is: ', gender_actor)

                            ##Extrair pontos de ator a partir de gênero. O código muda de acordo com o gênero.
                            try:
                                actor_points = soup1.find_all('div', attrs={"id":f'''filmo-head-{gen_act}'''})[0].a.next_sibling
                            except Exception as err0:
                                actor_points = 'null'
                                print(err0, ': ', gen_act)

                            actor_points_all.append(actor_points)
                            print("Actor points: ", actor_points)
                            print("""Actor page finished.
                            ---------------
                            """)
                
                ##Reminder: a = []
                #Movie specific infos scrapping:
                #name_code has the movies url.
                name_class = container.find('div', class_='lister-item-content')
                name_code = name_class.h3.a['href']
                name_code_all.append(name_code)

                #Get new response etc.
                response2 = requests.get(f'''https://www.imdb.com{name_code}''', headers = headers)
                soup2 = BS(response2.text, 'lxml')
                
                #Do sleep.
                sleep(randint(2,5))
                
                #Another information block:
                general1 = soup2.find_all("span", class_="ipc-metadata-list-item__label")

                #Now, we extract the wanted infos.
                #They were all under the same tree branch.
                #We needed to do loops to extract the wanted infos. 
                
                country_mov = ''
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if not "Countr" in z.text:
                            continue
                        if "Countr" in z.text:
                            country_mov = general1[i].next_sibling.text
                            print(country_mov)
                    except Exception:
                        break
                if country_mov == '':
                    country_mov = 'null'
                country_mov_all.append(country_mov)
                
                
                language_mov = ''
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if not "Language" in z.text:
                            continue
                        if "Language" in z.text:
                            language_mov = general1[i].next_sibling.text
                            print(language_mov)
                    except Exception:
                        break
                if language_mov == '':
                    language_mov = 'null'
                language_mov_all.append(language_mov)
                
                
                
                budget_mov = ''    
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if z.text != "Budget":
                            continue
                        if z.text == "Budget":
                            budget_mov = general1[i].next_sibling.text
                            print(budget_mov)
                    except Exception:
                        break
                if budget_mov == '':
                    budget_mov == 'null'
                budget_mov_all.append(budget_mov)

                
                
                gross_mov = ''    
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if z.text != "Gross US & Canada":
                            continue
                        if z.text == "Gross US & Canada":
                            gross_usa = general1[i].next_sibling.text
                            print(gross_usa)
                    except Exception:
                        break
                if gross_usa == '':
                    gross_usa == 'null'
                gross_usa_all.append(gross_usa)

                
                
                opening_week = ''
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if z.text != "Opening weekend US & Canada":
                            continue
                        if z.text == "Opening weekend US & Canada":
                            opening_week_us = general1[i].next_sibling.text
                            print(opening_week_us)
                    except Exception:
                        break
                if opening_week_us == '':
                    opening_week_us == 'null'
                opening_week_us_can_all.append(opening_week_us)

                
                
                world_gross = ''    
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if z.text != "Gross worldwide":
                            continue
                        if z.text == "Gross worldwide":
                            world_gross = general1[i].next_sibling.text
                            print(world_gross)
                    except Exception:
                        break
                if world_gross == '':
                    world_gross == 'null'
                gross_world_all.append(world_gross)

                
                
                genres_mov = ''  
                for i in range(0,30):
                    try:
                        z = general1[i]
                        if z.text != "Genres":
                            continue
                        if z.text == "Genres":
                            genres_mov = general1[i].next_sibling.text
                            print(genres_mov)
                    except Exception:
                        break
                if genres_mov == '':
                    genres_mov == 'null'
                genres_mov_all.append(genres_mov)
                             

                #Back to the original page (where the container was):
                
                year = container.h3.find('span', class_="lister-item-year text-muted unbold").text
                years_all.append(year)

                time = container.p.find('span', class_="runtime").text
                time_all.append(time)

                ratings = container.find('div', class_="ratings-bar")
                ratings_all.append(ratings)

                imdb = ratings.strong.text
                imdb_all.append(imdb)

                m_score = container.find('span', class_ = 'metascore').text
                metascore_all.append(int(m_score))
        
                final_section = container.find('p', class_="sort-num_votes-visible")
                final_section_all.append(final_section)

                conjunto_cod = final_section.find_all('span', attrs = {'name':'nv'})
                conjunto_cod_all.append(conjunto_cod)

                conjunto = [my_tag.text for my_tag in final_section.find_all('span', attrs = {'name':'nv'})]
                conjunto_all.append(conjunto)
                
                
                votes_all = [item[0] for item in conjunto_all]
                revenue_all = [item[-1] for item in conjunto_all]
                
                #Check if all infos are the same length.
                print(f"""
                names_all: {len(names_all)}
                actor_points_all: {len(actor_points_all)}
                year: {len(years_all)}
                duration: {len(time_all)}
                imdb: {len(imdb_all)}
                metascore: {len(metascore_all)}
                votes imdb: {len(metascore_all)}
                revenue gross: {len(revenue_all)}
                actor gender: {len(gender_actor_all)}
                director nation: {len(gender_actor_all)}
                actor nation: {len(place_birth_act_all)}
                actor placement: {len(actor_placement_all)}
                year birth director: {len(year_birth_direc_all)}
                year birth actor: {len(year_birth_act_all)}
                director points': {len(dic_points_all)}
                actor points': {len(actor_points_all)}
                'country of origin': {len(country_mov_all)}
                'movie language': {len(language_mov_all)}
                total budget': {len(budget_mov_all)}
                revenue gross USA': {len(gross_usa_all)}
                'revenue gross world': {len(gross_world_all)}
                revenue gross abertura USA&Canada': {len(opening_week_us_can_all)}
                """)
                
                #If they arent, the program will stop bc of error:
                are_arrays_equal = pd.DataFrame(
                {'movie': names_all,
                 'actor_gender': gender_actor_all,
                 'director nation': place_birth_direc_all,
                 'revenue gross abertura USA&Canada': opening_week_us_can_all
                })
                
                counter+=1

#Create the first dataFrame.
test_df = pd.DataFrame(
    {'movie': names_all,
     'year': years_all,
     'duration': time_all,
     'imdb': imdb_all,
     'metascore': metascore_all,
     'votes imdb': votes_all,
     'revenue gross': revenue_all,
     'actor_gender': gender_actor_all,
     'director nation': place_birth_direc_all,
     'actor nation': place_birth_act_all,
     'actor placement': actor_placement_all,
     'year birth director': year_birth_direc_all,
     'year birth actor': year_birth_act_all,
     'director points': dic_points_all,
     'actor points': actor_points_all,
     'country of origin': country_mov_all,
     'movie language': language_mov_all,
     'total budget': budget_mov_all,
     'revenue gross USA': gross_usa_all,
     'revenue gross world': gross_world_all,
     'revenue gross abertura USA&Canada': opening_week_us_can_all,
     'generos': genres_mov_all
    })

#Safety copy the dataFrame.
table1 = test_df.copy()

#Data cleaning.
table1.loc[:, 'year'] = table1['year'].str[-5:-1].astype(int)

table1['duration'] = [int(i.split()[0]) for i in table1['duration']]

table1['imdb'] = [float(i) for i in table1['imdb']]

table1['metascore'] = [int(i) for i in table1['metascore']]

table1['votes imdb'] = [int(i.replace(',', '')) for i in table1['votes imdb']]

table1['revenue gross'] = [float(i[1:-1]) if '$' in i else float(i.replace(',',''))*0.000001 for i in table1['revenue gross']]

table1['director nation'] = [i.split(',')[-1].strip() for i in table1['director nation']]

table1['actor nation'] = [i.split(',')[-1].strip() for i in table1['actor nation']]

table1['total budget'] = [i.split(' ')[0].replace(',', '').replace('/n', '').replace('$', '') for i in table1['total budget']]

table1['revenue gross USA'] = [i.replace(',', '').replace('$', '') for i in table1['revenue gross USA']]

table1['revenue gross world'] = [i.replace(',', '').replace('$', '') for i in table1['revenue gross world']]

table1['revenue gross abertura USA&Canada'] = [i.split(' ')[0].replace(',', '').replace('$', '')[:-3] for i in table1['revenue gross abertura USA&Canada']]

#In these vars, when there were more than one country, language and genre,
#they were stuck together, with an upper letter between then.
#We create a script to separate them and store the first info.
for j in range(len(table1['country of origin'])):
    text_splt = []
    country = ''
    for i in range(len(table1['country of origin'][j])):
        try:
            if table1['country of origin'][j][i].isupper():
                if table1['country of origin'][j][i-1] != ' ':
                    text_splt.append(country)
                    country = ''
                    country += table1['country of origin'][j][i]
                else:
                    country += table1['country of origin'][j][i]
            else:
                country += table1['country of origin'][j][i]
        except IndexError:
            country += table1['country of origin'][j][i]
    text_splt.append(country)
    try:
        table1['country of origin'][j] = text_splt[1]
    except IndexError:
        table1['country of origin'][j] = 'null'

for j in range(len(table1['movie language'])):
    text_splt = []
    country = ''
    for i in range(len(table1['movie language'][j])):
        try:
            if table1['movie language'][j][i].isupper():
                if table1['movie language'][j][i-1] != ' ':
                    text_splt.append(country)
                    country = ''
                    country += table1['movie language'][j][i]
                else:
                    country += table1['movie language'][j][i]
            else:
                country += table1['movie language'][j][i]
        except IndexError:
            country += table1['movie language'][j][i]
    text_splt.append(country)
    try:
        table1['movie language'][j] = text_splt[1]
    except IndexError:
        table1['movie language'][j] = 'null'
        
for j in range(len(table1['generos'])):
    text_splt = []
    country = ''
    for i in range(len(table1['generos'][j])):
        try:
            if table1['generos'][j][i].isupper():
                if table1['generos'][j][i-1] != ' ':
                    text_splt.append(country)
                    country = ''
                    country += table1['generos'][j][i]
                else:
                    country += table1['generos'][j][i]
            else:
                country += table1['generos'][j][i]
        except IndexError:
            country += table1['generos'][j][i]
    text_splt.append(country)
    print(text_splt)
    try:
        table1['generos'][j] = text_splt[1] 
    except IndexError:
        table1['generos'][j] = 'null'
print(table1['generos'])

#Continuing with the cleaning -> transforming strings to int.
for j in range(len(table1['movie'])):
    try:
        table1['year birth director'][j] = int(table1['year birth director'][j].replace('\n', ''))
    except Exception as err1:
        pass
    try:
        table1['year birth actor'][j] = int(table1['year birth actor'][j].replace('\n', ''))
    except Exception as err2:
        pass
    
    try: 
        table1['director points'][j] = int(table1['director points'][j][2:4])
    except Exception as err3:
        table1['director points'][j] = 'null'
        print('direc_points - deu ruim porque ', err3)

    try: 
        table1['actor points'][j] = int(table1['actor points'][j][2:4])
    except Exception as err4:
        table1['actor points'][j] = 'null'
        print('act_points - deu ruim porque ', err4)

    try: 
        table1['actor placement'][j] = int(table1['actor placement'][j])
    except Exception as err5:
        table1['actor placement'][j] = table1['actor placement'][j].replace('RANK', 'null')
       
    try:
        table1['year birth director'][j] = int(table1['year birth director'][j])
    except Exception as err6:
        table1['year birth director'][j] = 'null'
        print('yr birth dir deu ruim porque ', err6)
    try:
        table1['year birth actor'][j] = int(table1['year birth actor'][j])
    except Exception as err7:
        table1['year birth actor'][j] = 'null'
        print('yr birth act deu ruim porque ', err7)
        
    try:
        table1['total budget'][j] = int(table1['total budget'][j])
    except Exception as err8:
        table1['total budget'][j] = 'null'
    
    try:
        table1['revenue gross abertura USA&Canada'][j] = int(table1['revenue gross abertura USA&Canada'][j])
    except Exception as err8:
        table1['revenue gross abertura USA&Canada'][j] = 'null'
        
    try:
        table1['revenue gross world'][j] = int(table1['revenue gross world'][j])
    except Exception as err8:
        table1['revenue gross world'][j] = 'null'
    
    try:
        table1['revenue gross USA'][j] = int(table1['revenue gross USA'][j])
    except Exception as err8:
        table1['revenue gross USA'][j] = 'null'
        
        
##Joining gender columns:

data = {'director gender': gender_dic_all, 'director gender1': gender_dic1_all}
gender_df = pd.DataFrame(data=data)
temp = []
for i in range(len(gender_df['director gender'])):

    if gender_df['director gender'][i] == gender_df['director gender1'][i]:
        temp.append(gender_df['director gender'][i])
    elif gender_df['director gender'][i] == 'female' or gender_df['director gender1'][i] == 'female':
        temp.append('female')
    elif gender_df['director gender'][i] == 'not sure' and gender_df['director gender1'][i] != 'not sure':
        temp.append(gender_df['director gender1'][i])
    elif gender_df['director gender1'][i] == 'not sure' and gender_df['director gender'][i] != 'not sure':
        temp.append(gender_df['director gender'][i])
    else: temp.append('not sure')

gender_df['gender director'] = temp[:]
table1['gender director'] = gender_df['gender director']

#Converting to csv:
table1.to_csv('IMDB_scrapping.csv')
table1