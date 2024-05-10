import streamlit as st
import pandas as pd
import functions as git
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime , timedelta
import plotly.express as px

st.set_page_config(
    page_title="Github Dashboard",
    page_icon='github.png',
    initial_sidebar_state="expanded",
    layout="wide" ,
    menu_items={
    'About': ' Github repo link : \n test'
    }
)


def date_commits_extract():
    date_commites = []
    for user in list:
        inner = []
        for cord in user[6]:
            inner.append(cord[1])
        date_commites.append(inner)

    return date_commites



def making_liste(x):
    use = []
    for user in list:
        use.append(user[x])
    return use


def data2csv(data):
    data2csv = pd.DataFrame({
        "Owner": making_liste(0),
        "Owner ID": making_liste(3),
        "Repo Name": making_liste(9),
        "Repo URL": making_liste(1),
        "Stars": making_liste(2),
        "Commits": making_liste(4),
        "Contibuters": making_liste(5),
        "Forks": making_liste(7),
        "Last Commit": making_liste(8),

    })

    @st.cache_data
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(data2csv)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'Data_repos_in_{date}.csv',
        mime='text/csv',
        use_container_width=True
    )


def sub_title(s_title):
    colored_header(
        label=s_title,
        description=" ",
        color_name="light-blue-70",
    )
def option():
    colored_header(
        label="Set Your Optins ",
        description=" ",
        color_name="light-blue-70",
    )
def header_title():
    colored_header(
        label="GITHUB FILTER",
        description="The `GitHub Filter` uses `GitHub's API`  to collect and organize repository data by language, stars, and other criteria. It then provides customizable visualizations, such as line charts and erea charts, to analyze trends and insights within the GitHub ecosystem. This tool streamlines the process of discovering and understanding repository trends for developers and researchers.",
        color_name="light-blue-70",
    )



add_vertical_space(2)
actual_date = datetime.now().date()

with st.sidebar :

    date = st.date_input("Select A date to fetsh : ")
    st.write(' Fetching day : ', date)

    language = st.text_input("Tape a Language : ")
    st.markdown(f"""
                Language selected : `{language.capitalize()}`
                """)
    language = language.upper()
    max_commits = st.slider('Select Max of commits to fetch ?', 0, 10000, 100)
    st.write("Max Commits selected : ", max_commits, ' Commits')

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = True

    st.checkbox("Enable Commit Box", key="disabled")

    option = st.selectbox(
    " Active This ?",
    (" Day", "Last Week", "Last Month","Last Year"),
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
        )
    if st.session_state['disabled'] :
        search_str = 'nothing'

    else :
        if option == ' Day' :
            search =   datetime.now().date() + timedelta(days=0)
            search_str = search.strftime("%Y-%m-%d")

        elif option == 'Last Week':
            search = datetime.now().date() + timedelta(days=-7)
            search_str = search.strftime("%Y-%m-%d")


        elif option == 'Last Month' :
            search =   datetime.now().date() + timedelta(days=-30)
            search_str = search.strftime("%Y-%m-%d")
        else :
            search = datetime.now().date() + timedelta(days=-365)
            search_str = search.strftime("%Y-%m-%d")

if st.sidebar.button(' Start Fetshing ', use_container_width=True) :
    if date <= actual_date:
        with st.spinner('Wait for it...'):
            start_time = datetime.now()
            repo_found = 0
            list , repo_found , total_repos , colect_langs = git.fetch_trendy(date, language, max_commits , search_str)
            end_time = datetime.now()
            time_difference = end_time - start_time
            hours = time_difference.seconds // 3600
            minutes = (time_difference.seconds % 3600) // 60
            seconds = time_difference.seconds % 60
            final_date = f"{str(hours).zfill(2)} : {str(minutes).zfill(2)} : {str(seconds).zfill(2)}"
            part1 , part2 = st.container().columns(2)

            with part1 :
                add_vertical_space(10)
                col1, col2 , col3 = st.columns(3)
                col1.metric(label="Total Number of Repositories Found", value=f"{total_repos}")
                col2.metric(label="Targeted Repositories", value=f"{repo_found}")
                col3.metric(label="Time Spent ", value=f"{final_date}")
                style_metric_cards("#154360", 0, "#154360", 5, "#030303", True)
            # print(list)
            with part2 :
                used_langs = [lg[0] for lg in colect_langs]
                used_number = [lg[1] for lg in colect_langs]
                di_langs = {
                    "Language": used_langs,
                    "NumberOfUse": used_number
                }
                df_langs = pd.DataFrame(di_langs)
                df_langs = df_langs.sort_values(by='NumberOfUse' , ascending=False)
                df_langs= df_langs.head(7)
                dia = px.pie(df_langs, values="NumberOfUse", names="Language",   hole=0.3)
                dia.update_layout(
                    title="Top 7 of Used Languages In This Search" ,
                    title_x=0.3,
                    title_y=0.05,
                    legend=dict(
                        title="Languages",
                        orientation="v",
                        y=0,
                        xanchor="right",
                        x=1,
                    )
                )
                con = st.container()
                con.write(dia)

            sub_title("Key Repository Metrics (DATA FRAME)")

            # data frame for streamlit_extras dataframe

            data_frame_1 = pd.DataFrame({
                "Owner": making_liste(0),
                "Stars": making_liste(2),
                "Forks" : making_liste(7),
                "Commits": making_liste(4),

            })

            st.dataframe(
                data_frame_1,
                column_config={
                    "Owner": st.column_config.ListColumn("Owner", width="large", ),
                    "Commits": st.column_config.NumberColumn(
                        "Commits",
                        help="Number of commits on GitHub",
                        format=" %s 📑",
                    ),
                    "Stars": st.column_config.NumberColumn(
                        "Stars",
                        help="Number of stars on GitHub",
                        format=" %s ⭐",
                    ),
                    "Forks": st.column_config.NumberColumn(
                        "Forks",
                        help="Number of forks on GitHub",
                        format=" %s  👥",
                    ),
                },
                hide_index=True,use_container_width = True
            )

            add_vertical_space(2)
            sub_title("Key Repository Metrics (PLOTING CHARTS)")
            add_vertical_space(2)
            trans = [ making_liste(4), making_liste(7) ]
            transposed_list = [[x, y] for x, y in zip(*trans)]
            transposed_list.insert(0,[0,0])

            con_char = st.container()
            char1, char2 = con_char.columns(2)
            index_char1 = making_liste(0)
            index_char1.insert(0,"")
            # index_char1.append("")

            with char1 :
                add_vertical_space(2)
                chart_data = pd.DataFrame(  transposed_list , index= index_char1  ,columns = [" Number Of Commits", " Number Of Forks"]  )
                st.area_chart( chart_data , color=[ "#0066ff" ,"#1affff"] )


            owners = [ str(elem[0]) for elem in list]
            # owners.append("^")
            owners.insert(0,"")
            nmbr_stars = [ elem[2] for elem in list]
            # nmbr_stars.append(0)
            nmbr_stars.insert(0,0)
            data2plot = pd.DataFrame({
                "Owner": owners,
                " Number Of Stars": nmbr_stars ,
            })

            with char2 :
                data2plot.set_index("Owner", inplace=True)
                # st.line_chart(data2plot)
                st.line_chart(
                    data2plot,  color=["#00ffff"]
                )
        #commit section :
            add_vertical_space(2)
            sub_title("Repo Activity details ")
            add_vertical_space(2)
            data_frame_commit = pd.DataFrame({
                "Repo Name": making_liste(9),
                "Commits": making_liste(4),
                "Last Commit" : making_liste(8) ,
                "Activity Date": date_commits_extract(),
            })
            st.dataframe(
                data_frame_commit,
                column_config={
                    "Repo Name":st.column_config.ListColumn( "Repo Name" ),
                    "Commits": st.column_config.NumberColumn(
                        "Commits",
                        help="Number of commits on GitHub",
                        format=" %s 📑",
                    ),
                    "Last Commit" : st.column_config.ListColumn(
                                   "Last Commit"

                     ),
                    "Activity Date": st.column_config.LineChartColumn(
                        "Activity Range ", y_min=0, y_max=10
                    ),
                },
                hide_index=True,use_container_width = True
            )

            # data frame for all data
            add_vertical_space(2)
            sub_title("More Informations ")
            add_vertical_space(2)
            str_list = [str(num) for num in making_liste(3)]

            data_frame_2 = pd.DataFrame({
                "Owner ID": str_list,
                "Owner": making_liste(0),
                "Repo Name": making_liste(9),
                "Repository Link": making_liste(1),
                "List of Contributers": making_liste(5),

            })
            st.dataframe(
                data_frame_2,
                column_config={
                    "Owner ID": st.column_config.ListColumn("Owner ID", ),
                    "Owner": st.column_config.ListColumn("Owner", ),
                    "Repo Name": st.column_config.ListColumn("Repo Name"),
                    "Repository Link": st.column_config.LinkColumn("Repo URL"),
                    "List of Contributers": st.column_config.ListColumn("Contributers")
                },
                hide_index=True, use_container_width=True
            )

        with st.sidebar :
            add_vertical_space(2)
            st.subheader('To Download the retrieved Data as a ` CSV File` ')
            sub_title('')
            add_vertical_space(1)
            data2csv(list)



        st.success('Done!!')

        add_vertical_space(2)
        def example_github():
            badge(type="github", name="streamlit/streamlit")
        example_github()
    else :
        st.error("Please ensure that you choose a date from the past or today date. Only past/today dates are valid for this operation.")


else :
    header_title()


