from functions.MDR.device_MDR_xml import device_MDR_xml
from functions.MDR.UDIDI_MDR_xml  import UDIDI_MDR_xml
from functions.MDR.POST_upload_BasicUDIDI_MDR_xml import POST_upload_BasicUDIDI_MDR_xml
from functions.MDR.POST_upload_UDIDI_for_existing_BasicUDIDI_MDR_xml  import POST_upload_UDIDI_for_existing_BasicUDIDI_MDR_xml
#from category_rules import RULES
import xml.etree.ElementTree as ET
import pandas as pd
import re

#load excel
df = pd.read_excel("data_UDIDI/Database MDR_carbide burs.xlsx", sheet_name="Base1", dtype=str, header=2)  # first sheet
print(df.columns)
df = df.astype(str)
df = df.replace({
    "VRAI": "true",
    "FAUX": "false",
    "True": "true",
    "False": "false"
})
devices = []
compteur = 0
id = 1

for _, row in df.iterrows():
    manufacturer_code = "CH-MF-000033901"
    authorisedRepresentative_code = "FR-AR-000032502"
    device = device_MDR_xml(
            risk_class = "CLASS_IIA",
            model = row["Device_Model*"],
            name = row["Device_Name*"],
            primary_DI = row["Basic_UDI*"],
            manufacturer_code = manufacturer_code,
            authorisedRepresentative_code = authorisedRepresentative_code,
            basic_UDIDI = row["UDI_DI*"],
            reference = row["Reference_Catalogue_Number*"],
            trade_name = row["Trade_name*"],
            description = row["Additional_Product_Description*"],
            mdn_code =  row["MDNCode*"],
            sterilization = "true",
            number_of_reuses = row["Max_Number_Of_Reuses*"],
            reusable = row["MDR_Reusable_Surgical_Instruments*"],
            diameter = row["Value_text*.1"],
            length = row["Value_text*"],
            #packaging_DI = "?",#row[""],
            number_of_items = row["Quantity_of_Device*"],
            start_date="2020-02-01+01:00"
    )
    devices.append(device)
    compteur = compteur+1

    if compteur == 299:
        push_xml = POST_upload_BasicUDIDI_MDR_xml(
            devices_xml_list = devices,
            #service_token="YOUR_TOKEN",
            sender_actor_code= manufacturer_code,#"CH-MF-000016224", #CH-MF-000016224
            #sender_party_id="YOUR_PARTY_ID"
        )
        name = "eudamed_push_carbure_" + str(id) + ".xml"
        id = id+1

        tree = ET.ElementTree(push_xml)
        ET.indent(tree, space="    ", level=0)
        tree.write(
            name,
            encoding="utf-8",
            xml_declaration=True
        )
        devices = []
        compteur = 0

push_xml = POST_upload_BasicUDIDI_MDR_xml(
    devices_xml_list = devices,
    #service_token="YOUR_TOKEN",
    sender_actor_code= manufacturer_code,#"CH-MF-000016224", #CH-MF-000016224
    #sender_party_id="YOUR_PARTY_ID"
    )
name = "eudamed_push_carbure_" + str(id) + ".xml"
id = id+1
        
tree = ET.ElementTree(push_xml)
ET.indent(tree, space="    ", level=0)
tree.write(
        name,
        encoding="utf-8",
        xml_declaration=True
    )
