import streamlit as st
import streamlit.components.v1 as components


#st.download_button(
    #    label="Save xml file",
    #    data=xml,
    #    file_name=file_name,
    #    mime='text/xml',
    #)

def get_saveas(xml):
    
            
    js = (
        """
            <button type="button" id="picker">Save XML</button>

            <script>

            async function run() {
                console.log("Running")
            const handle = await showSaveFilePicker({
                suggestedName: 'my_xml.xml',
                types: [{
                    description: 'CSV Data',
                    accept: {'text/plain': ['.xml']},
                }],
            });
            """
                + f"const blob = new Blob([`{xml}`]);"
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
        