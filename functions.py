import requests as rq
from datetime  import datetime ,timedelta
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("GIT_TOKEN")
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github.v3+json'
}

colect_langs  = []
def collect_language(langgs) :
    for lg in langgs.keys():
        exist = 0
        if len(colect_langs) != 0  :
            for co in colect_langs:
                if co[0] == lg :
                    co[1] += 1
                    exist = 1
            if exist == 0 :
                colect_langs.append([lg,1])
        else :
            colect_langs.append([lg, 1])


    return colect_langs




def get_all_commits( url):
    commits = []
    while url:
        response = rq.get(url, headers=headers)
        commits.extend(response.json())
        url = response.links.get("next", {}).get("url")

    return commits




def get_table_dates_commits_number(url,max_commits):
    all_commits = get_all_commits(url)
    last_commit=all_commits[0]['commit']['committer']['date'].split('T')[0]
    # print("Total number of commits:", len(all_commits))
    if(len(all_commits) < max_commits):
        commit_date0 = all_commits[0]['commit']['committer']['date'].split('T')[0]
        i= 0
        list = []
        # print("commit date ref  " ,commit_date0)
        for commit in all_commits:
            commit_date   = commit['commit']['committer']['date'].split('T')[0]
            if commit_date == commit_date0 :
                i+=1
            else :
                list.append([commit_date0,i])
                commit_date0 = commit_date
                i=1
        list.append([commit_date0,i])

    else :
        return 0 , [] , 0 , ""
    return   len(all_commits) , list , len(list) , last_commit

def rm_empty_lists(outer_list) :
    filtered_list = [inner_list for inner_list in outer_list if inner_list]
    return  filtered_list

def find_contri(url) :
    r = rq.get(url , headers=headers)
    contributers = []
    for user in r.json() :
        contributers.append(user["login"])
    return  contributers

def fetch_trendy(date,language,max_commits,search_str):
        url=f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc"

        # print(url)
        r = rq.get(url)
        # print(r.status_code)
        filtred = []

        if r.status_code == 200 :
            items = r.json()["items"]
            total_repos = len(r.json()["items"])
            i=0
            for item in items :
                print(i)
                i+=1

                username , repo_link , langs , stars ,id_repo ,commits_url , contr = item['owner']['login'],item['html_url'],item["languages_url"] , item['stargazers_count'] , item["id"] , item['commits_url'][:-6] , item["contributors_url"]
                url_lang = f"{langs}"
                r_lang = rq.get(url_lang, headers=headers)
                if r_lang.status_code == 200:
                    lang_used = r_lang.json()

                    if language != "" :
                            collect_language(lang_used)
                            for key in lang_used.keys():
                                if key.upper() == language  :
                                    nmr_commit, list_dates_of_commits, max_of_commits ,last_commit = get_table_dates_commits_number(item['commits_url'][:-6] , max_commits)
                                    fork = item['forks_count']
                                    name = item['name']
                                    list_conti  =  find_contri(contr)
                                    if search_str <= last_commit or search_str == 'nothing' :
                                        if len(list_dates_of_commits) > 2  :
                                            data = [username, repo_link, stars, id_repo, nmr_commit, list_conti,
                                                    list_dates_of_commits, fork , last_commit , name]
                                            filtred.append(data)
                                        elif (len(list_dates_of_commits) == 1 or len(list_dates_of_commits) == 2   )  :
                                            date1 = [datetime.now().date().strftime("%Y-%m-%d"), 0]
                                            date2 = datetime.now().date() + timedelta(days=1)
                                            date2_str = date2.strftime("%Y-%m-%d")
                                            my_list2 = [date2_str, 0]
                                            list_dates_of_commits.append(date1)
                                            list_dates_of_commits.append(my_list2)
                                            data = [username, repo_link, stars, id_repo, nmr_commit, list_conti,
                                                    list_dates_of_commits, fork , last_commit , name ]
                                            filtred.append(data)
                    else :
                        collect_language(lang_used)
                        nmr_commit, list_dates_of_commits, max_of_commits, last_commit = get_table_dates_commits_number(item['commits_url'][:-6], max_commits)
                        fork = item['forks_count']
                        name = item['name']
                        list_conti = find_contri(contr)
                        if search_str <= last_commit or search_str == 'nothing':
                            if len(list_dates_of_commits) > 2:
                                data = [username, repo_link, stars, id_repo, nmr_commit, list_conti,
                                        list_dates_of_commits, fork, last_commit, name]
                                filtred.append(data)
                            elif (len(list_dates_of_commits) == 1 or len(list_dates_of_commits) == 2):
                                date1 = [datetime.now().date().strftime("%Y-%m-%d"), 0]
                                date2 = datetime.now().date() + timedelta(days=1)
                                date2_str = date2.strftime("%Y-%m-%d")
                                my_list2 = [date2_str, 0]
                                list_dates_of_commits.append(date1)
                                list_dates_of_commits.append(my_list2)
                                data = [username, repo_link, stars, id_repo, nmr_commit, list_conti,
                                        list_dates_of_commits, fork, last_commit, name]
                                filtred.append(data)


        max = 0
        for elem in filtred:
            if max < len(elem[6]):
                max = len(elem[6])

        for elem in filtred:
            i = len(elem[6])
            d = 0
            while i < max:
                date2 = datetime.now().date() + timedelta(days=d)
                date2_str = date2.strftime("%Y-%m-%d")
                my_list2 = [date2_str, 0]
                elem[6].append(my_list2)
                i += 1
                d += 1
        # print(len(filtred))
        # print(filtred)
        return  filtred, len(filtred) , total_repos ,colect_langs










































