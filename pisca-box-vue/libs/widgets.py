import base64
import streamlit as st


def show_pdf(file_path,height=800):
    with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="{height}" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def page_header(title,divider=True, other_icon="gift"):
    st.set_page_config(page_title='pisca-box', page_icon = 'app/static/pb.png',
            layout = 'wide', initial_sidebar_state = 'auto')
    st.markdown('<style>section[data-testid="stSidebar"] {width: 10px !important; # Set the width to your desired value}</style>',unsafe_allow_html=True,)
    if other_icon == "gift":
        st.title(f':gift: {title}')
    elif other_icon == "mirror":
        st.title(f':mirror: {title}')
    elif other_icon == "tree":
        st.title(f':deciduous_tree: {title}')
    elif other_icon == "plot":
        st.title(f':frame_with_picture: {title}')
    else:
        st.title(f':gift: {title}')
    #if divider:
    #    st.divider()
    


def get_saveas(big_str,nam,ext="xml",button_text="Save XML"):
    
            
    js = (
            f'<button type="button" id="picker" style="z-index:99;position:relative">{button_text}</button>'
            +"""

            <script>

            async function run() {
                console.log("Running")
            const handle = await showSaveFilePicker({
                """
                + f"suggestedName: '{nam}.{ext}',"
                +"""
                types: [{
                    description: '',
                """
                + 'accept: {"text/plain": [".' + ext + '"]},'
                +"""
                }],
            });
            """
                + f"const blob = new Blob([`{big_str}`]);"
                + """

            const writableStream = await handle.createWritable();
            await writableStream.write(blob);
            await writableStream.close();
            }

            document.getElementById("picker").onclick = run
            console.log("Done")
            </script>

            """
        )

    return js



        

    