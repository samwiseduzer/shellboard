import streamlit as st
import subprocess
from os import system

def speak(msg, speaker, rate):
    if msg:
        system(f'say -v {speaker} -r {str(rate)} \"{msg}\"')

def live_form():
    with st.expander('Live'):
        st.session_state.old_live_text = st.session_state.live_text if 'live_text' in st.session_state.keys() else ''
        st.session_state.rate = st.session_state.rate if 'rate' in st.session_state.keys() else 100

        col1, col2, col3, col4 = st.columns((8,2,1,1))

        speaker = col2.selectbox(
            "Speaker",
            ("Karen", "Evan", "Jamie", "Samantha", "Viktor", "Zarvox"),
            key="live_text_speaker"
        )
        rate = col2.select_slider(
            "Words per minute",
            options=(50,75,100,125,150,175,200,300),
            key="rate"
        )

        def handle_live_text_change():
            if st.session_state.live_text != st.session_state.old_live_text:
                speak(st.session_state.live_text, st.session_state.live_text_speaker, st.session_state.rate)

        def clear_text():
            st.session_state['live_text'] = ''

        text = col1.text_area('live', key='live_text', on_change=handle_live_text_change)
        if text:
            col1.button('run', on_click=lambda: speak(text, speaker, rate))
            col1.button('clear_live', on_click=clear_text)
        with col1.container():
            st.write('Prepared dialogue')
            col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8 = st.columns(8)
            
            for i, d in enumerate(st.session_state.dialogs):
                match ((i+1) % 8):
                    case 0:
                        target = col_8
                        d['col'] = 8
                    case 7:
                        target = col_7
                        d['col'] = 7
                    case 6:
                        target = col_6
                        d['col'] = 6
                    case 5:
                        target = col_5
                        d['col'] = 5
                    case 4:
                        target = col_4
                        d['col'] = 4
                    case 3:
                        target = col_3
                        d['col'] = 3
                    case 2:
                        target = col_2
                        d['col'] = 2
                    case 1:
                        target = col_1
                        d['col'] = 1

                target.button(
                    d['title'],
                    help=d['text'],
                    on_click=lambda x: speak(x['text'], speaker, rate),
                    args=[d],
                    key=d['title']+'_'+d['text']
                )
                
        col3.button('Yes', on_click=lambda: speak('Yes', speaker, st.session_state.rate))
        col3.button('No', on_click=lambda: speak('No', speaker, st.session_state.rate))
        col3.button('Voice gone', on_click=lambda: speak('I\'ve completely lost my voice so I\'m using this app to speak for me.', speaker, st.session_state.rate))
        col3.button('This app', on_click=lambda: speak('This app uses streamlit to call a subprocess that leverages OSX\'s built-in voice synthesizers.', speaker, st.session_state.rate))

        col4.button('Howdy folks!', on_click=lambda: speak('Howdy, folks!', speaker, st.session_state.rate))
        col4.button('Hi!', on_click=lambda: speak('Hi, how are you doing!', speaker, st.session_state.rate))
        col4.button('Alright', on_click=lambda: speak('I\'m doing alright!', speaker, st.session_state.rate))



def prepared_dialogue():
    def save():
        st.session_state.dialogs.append({
            "title": st.session_state.new_title,
            "text": st.session_state.new_text
        })
        st.session_state.new_title = ''
        st.session_state.new_text = ''

    with st.expander('Prepare Dialogue'):
        title = st.text_input('title', key="new_title")
        text = st.text_area('text', key="new_text")
        st.button('Save', on_click=save)

def init():
    st.session_state.dialogs = st.session_state.dialogs if 'dialogs' in st.session_state else []

def main():
    st.set_page_config(layout="wide")
    st.title('Test')
   
    init()
    live_form()
    prepared_dialogue()
    

if __name__ == "__main__":
    main()

