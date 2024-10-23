import streamlit as st
import librosa
import soundfile as sf
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# Config streamlit page
st.set_page_config(
    page_title="GoodWine - Découvrez l'excellence d'un son bio🌿",
    page_icon="🍇",
    layout="centered",
)

# CSS
st.markdown("""       
    <style>    
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@900&family=Inter:wght@400;600;700&display=swap');
        
        /* Arrière-plan animé */
        @keyframes gradientAnimation {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
            
        /* Credit animé */
        @keyframes modernAnimation {
            0% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }

        /* Header streamlit */
        .stApp {
            background: linear-gradient(270deg, #FFCC80, #FF6F61, #D17D99, #C29BBA); /* Jaune et orange plus pâles */
            background-size: 400% 400%;
            animation: gradientAnimation 26s ease infinite;
        }
            
        .stAppHeader {
            display: none;
        }

        .title {
            text-align: center;
            color: #FEE7F0;
            font-size: 103px;
            font-weight: 900;
            font-style: italic;
            padding: 10px;
            border-radius: 5px;
            -webkit-text-stroke: 0.3px black;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            font-family: 'Merriweather', serif;
        }
                
        .paragraph {
            color: #FEE7F0;
            font-size: 15px;
            padding: 10px;
            border-radius: 0.1px;
            -webkit-text-stroke: 0.1px black;
            text-shadow: 0.5px 0.5px 1px rgba(0, 0, 0, 0.5);
            font-family: 'Merriweather', serif;
        } 
            
        .paragraph2 {
            text-align: center;
            color: #FEE7F0;
            font-size: 14px;
            padding-top: 2px;
            border-radius: 0.1px;
        } 

        .content-container {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            margin: 20px;
        }
            
        .credit_effect {
            position: fixed;
            bottom: 30px;
            right: 40px;
            font-size: 19px;
            font-family: 'Merriweather', serif;
            font-color: #FDD3E2;
            text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.5);
            border-radius: 2.5px;
            padding: 2.5px 5px;
            animation: modernAnimation 2.1s ease-in-out infinite;
            text-decoration: none;
        }
            
        .credit_effect:hover {
            color: #FEE7F0;
            text-decoration: none;
        }
        
        .credit_effect:visited {
            color: #FEE7F0;
            text-decoration: none;
        }
        
    </style>     
""", unsafe_allow_html=True)


st.markdown("""
    <h1 class="title">GoodWine</h1>
""", unsafe_allow_html=True)


st.markdown("""
    <p class="paragraph"> Rien de plus goûtu qu'une mélodie bien raffiné ! Flex tes sons comme un bon verre de vin rouge. Vinifie ta grappe et mets la toi meme en bouteille. </p>
""", unsafe_allow_html=True)


audio_file = st.file_uploader("Choose a wav file", type=["mp3", "wav", "m4a"])


if audio_file is not None:

    st.toast("Vinification terminée !")
    y, sr = librosa.load(audio_file, sr=None)


    # Barre de régulation de la vitesse du son
    speed = st.slider("Pressurage speed", 0.25, 2.0, 1.0, 0.01)
    y_fast = librosa.effects.time_stretch(y, rate=speed)


    # Maj auto du son modifié
    output = BytesIO()
    sf.write(output, y_fast, sr, format='WAV')
    output.seek(0)


    # Lecture de l'audio
    st.audio(output, format='audio/mp3')


    # Détection du tempo
    tempo, _ = librosa.beat.beat_track(y=y_fast, sr=sr)
    st.markdown(
        f"<p class='paragraph2'>Tempo détecté : {tempo[0]:.2f} BPM</p>"
    , unsafe_allow_html=True)


    st.session_state.show_plot=False
    if st.button("Afficher le Signal Audio"):
        st.session_state.show_plot = not st.session_state.show_plot 

    if 'show_plot' in st.session_state and st.session_state.show_plot:
        
        duree = len(y_fast) / sr
       
        # Downsample
        n = 5
        y_visual = y_fast[::n]  # Downsampled audio
        times_visual = np.arange(len(y_visual)) * (1 / sr) * n

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=times_visual,
            y=y_visual,
            mode='lines',
            name='Egrappage Audio',
            line=dict(color='#FF4B4B'),
            hoverinfo='text',
            hovertext=[
                f'Time: {t:.2f}s<br>Amplitude: {y[int(i * n)]:.2f}'  # Use original y for amplitude
                for i, t in enumerate(times_visual)  # Using downsampled times for hover
            ]
        ))

        # Update layout
        fig.update_layout(
            title='Signal Audio',
            xaxis_title='Temps (s)',
            yaxis_title='Amplitude',
            xaxis=dict(range=[0, duree]),  # Set x-axis range to total duration
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            height=400
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)


st.markdown("""
    <a class="credit_effect" href="https://github.com/ThibautEscalante" target="_blank"> 
        credit T.Escalante  
    </a>
""", unsafe_allow_html=True)


