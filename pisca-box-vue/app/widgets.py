

#st.download_button(
    #    label="Save xml file",
    #    data=xml,
    #    file_name=file_name,
    #    mime='text/xml',
    #)

def get_saveas(big_str,nam,ext="xml",button_text="Save XML"):
    
            
    js = (        
            f'<button type="button" id="picker">{button_text}</button>'
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
        