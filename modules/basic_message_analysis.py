# basic_message_analysis.py
from flask import render_template, request, jsonify
from enum import Enum
from static.python import trigram_helper
from static.python.trigram_helper import TrigramReadMode, EyeData


class Message(Enum):
    EAST_1 = "East 1"
    WEST_1 = "West 1"
    EAST_2 = "East 2"
    WEST_2 = "West 2"
    EAST_3 = "East 3"
    WEST_3 = "West 3"
    EAST_4 = "East 4"
    WEST_4 = "West 4"
    EAST_5 = "East 5"


messages = {
    Message.EAST_1: "20101322330404113023211431303300402400050320412200014222421222201100032013411135310221044000200104040144142033022034241523131313003113212014223133144134144121150140032121141300411101002412410040310015040331432341122101010040120412442442402513331220330103113111211210322314513104242241303041102031232043135",
    Message.WEST_1: "31101322330404113023211431303300402400450320412200014222421222201100032013411015020201044000104044040144142033022034131511121313000110202014223133144134144140152122233032440002432311102212310310220435403431401222111340210301413341221330132502414221422203024200123212402323201403531013221121302032222004223103132241135",
    Message.EAST_2: "1210132233040411302321143130330040240045132041220001422242122220110003201341132530201323004421014300121414031102410422351024411132222314033301302310103224414225014113030144102020311114241034232132112514112012004010302212240204000010322104050011322100422310432420131030102003002215020142240312031330231000103310441201422503420104310110020012451314020220201413223115",
    Message.WEST_2: "30101430423111113010320011421114204214451320410024412002221410132400222201204025110120210044012022014100202130013243312540113011201032231343142231321303110000351431102230242242010212231422001031112235203401230041222213132220230242140211440512220100001214310123331201022420322150110101013212311030320302413203220305",
    Message.EAST_3: "221014304000100302220231222232144144211533204100222243134100324200001022004243153132233121201340041413023100012310431305020020140002021212311100003112220110032514021422202304200121424121122310401003450030210313002122103100003123320032404225001240241020232043043031224131312301142523231113021102102022234141211324032123050010301242212240330032110242131332310015410210103300432031412111422330403400041504124012304504230101045",
    Message.WEST_3: "1110143040440231010332321201132400320235432041002342120301441212222401420211130503303113422414411130300314223404213111254314132002101412021124312302031114300215103133214200230011143034143033110122120510113221112044231013132123102031102220051201201231300110240141330210230022200445210312220001440122003232142141332131220512022402223420303312024404020050021211001411022421034024114425",
    Message.EAST_4: "1010143040001000000102132331201421330035232041002222431212430430300110203421130510100422321003430014421422402220030002253034110223132024033020302224411420101415143234300120242230110301302001040030130501233240134134130244130141241222230332252122221431303020131021131022300031032325432331411032403200122103112431440120231512202423010131123221303534212102201003230340345",
    Message.WEST_4: "3010143040001000000102132331201400400025232041002222431212430430300110222113142521131021400103212224112430010013122331350302212301323014304134203000323324211405040210240103202210243021012103012033232540221110313241210214244031112202143114152042332412033020233010412042410122321015311140311421232122410240132440030221440522431411404212111414013050202310000310001021400115",
    Message.EAST_5: "1110143040001000000102132331201430441335332041002222431212430430300110211112430510121422330202401414421222223021221323353034110224012020413020022424202403412025014110114103111010240110204010013100130521121113011044121111240341012204004121351020410412211341301330132430110420102215020203002240010120442311042111142031102513122422022204152324421013314315"
}

selected_mode = TrigramReadMode.ACB
selected_message = Message.EAST_1.name


def analyze_message_content(message_content):
    analyzed_content = []
    lines = message_content.split('5')
    for line in lines:
        if line:
            image_paths = [f"static/resources/images/eyes/eye_{char}.png alt='{char}'" for char in line if
                           char.isdigit() and char != '5']
            analyzed_content.append(image_paths)
    return analyzed_content


trigram_selection_path = f"static/resources/images/silmat-trigram-overlay.png"


def generate_message_html(analyzed_content, original_message):
    # Add the editor pane for text editing
    plaintext_message = original_message.replace("5", "\n")
    eye_data = EyeData("data", original_message, selected_mode)
    trigram_message = eye_data.get_raw_trigram_data()
    ascii_message = eye_data.get_trigram_values()

    html = '<table><tr><th>'
    html += '<div class="eye-images-container">'
    trigram_index = 0
    for i, line_images in enumerate(analyzed_content):
        html += '<div class="offset-images">' if i % 2 == 1 else '<div class="eye-images">'
        for j, image_path in enumerate(line_images):
            # Remove the leading forward slash from image_path
            html += f'<img src={image_path}>'
            if i % 2 == 0:

                trigram_val_list = trigram_message.replace("\n",",").split(",")

                if j % 3 == 0:
                    html += f'<img class="overlay-image" style="transform: translateX(-26px) translateY(2px);" src={trigram_selection_path} alt="{trigram_val_list.__getitem__(trigram_index)}">'
                    trigram_index = min(trigram_index + 1, len(trigram_val_list)-1)
                if j % 3 == 1 and j != len(line_images)-1:
                    html += f'<img class="overlay-image-flipped" style="transform: translateX(-12px) translateY(2px) rotate(180deg);" src={trigram_selection_path} alt="{trigram_val_list.__getitem__(trigram_index)}">'
                    trigram_index = min(trigram_index + 1, len(trigram_val_list)-1)

        html += '</div>'
    html += '</div></th></tr><tr><th>'

    # Direct Message Data
    html += f'<div id="eye_editor_pane" class="eye-editor-pane"><label><textarea wrap="off" class="editor-textarea">{plaintext_message}</textarea></label></div>'

    # Direct Trigram Data
    html += f'<div id="eye_editor_pane" class="eye-editor-pane"><label><textarea wrap="off" class="editor-textarea">{trigram_message}</textarea></label></div>'

    # Direct Ascii Data
    html += f'<div id="eye_editor_pane" class="eye-editor-pane"><label><textarea wrap="off" class="editor-textarea">{ascii_message}</textarea></label></div>'

    html += '</th></tr></table>'
    return html


def analyze_messages():
    analyzed_messages = {}
    for message, content in messages.items():
        analyzed_content = analyze_message_content(content)
        analyzed_html = generate_message_html(analyzed_content, content)
        analyzed_messages[message] = analyzed_html
    return analyzed_messages


def basic_analysis_page():
    number_of_panes = 3  # Define the number of panes
    if request.method == 'POST':
        message = request.json.get('message')
        mode = request.json.get('mode')

        global selected_message

        if mode is not None:
            global selected_mode
            selected_mode = TrigramReadMode[mode.split('.')[-1]]
        if message is not None:
            selected_message = message

        message_content = messages.get(Message[selected_message])
        analyzed_content = analyze_message_content(message_content)
        html_content = generate_message_html(analyzed_content, message_content)
        return jsonify(html_content)
    else:
        return render_template('html-pages/basic_message_analysis.html', Messages=Message,
                               number_of_panes=number_of_panes, trigram_modes=TrigramReadMode)
