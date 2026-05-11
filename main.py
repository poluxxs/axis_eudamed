from create_device_xml import create_device_xml
from create_push_xml  import create_push_xml
#from category_rules import RULES
import xml.etree.ElementTree as ET
import pandas as pd
import re

#load excel
df = pd.read_excel("data_UDIDI/Database.xlsx", sheet_name=0, dtype=str, header=2)  # first sheet
print(df.columns)
df = df.astype(str)
df = df.replace({
    "VRAI": "true",
    "FAUX": "false",
    "True": "true",
    "False": "false"
})
devices = []


for _, row in df.iterrows():
    #desc = str(row["Nom du marque [fr]"]).upper()

    # default values (important!)
    #mdn_code = None
    #number_of_reuses = None
    #primary_DI = None

    #for rule in RULES:
    #    pattern = rf"{rule['keyword']}\d*"
    #    if re.search(pattern, desc):
    #        mdn_code = rule["mdn_code"]
    #        number_of_reuses = rule["number_of_reuses"]
    #        primary_DI = rule["primary_DI"]
    #        break  # stop at first match

    # optional: handle no match
    #if primary_DI is None:
    #    raise ValueError(f"No rule matched for description: {desc}")

    manufacturer_code = "CH-MF-000016224"

    device = create_device_xml(
        risk_class = "CLASS_IIA",
        model = row["Device_Model*"],
        name = row["Device_Name*"],
        primary_DI = row["Basic_UDI*"],
        manufacturer_code = manufacturer_code,
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
    #break for tests
    break

# Example usage
#Wrench = create_device_xml(
#    risk_class="CLASS_I",
#    description_short="Wrench for US tips",
#    primary_DI="76309582WRENCXN",
#    basic_UDIDI="07630958213974",
#    #reference="Wrench IC",
   # trade_name="Torque wrench ICP W",
  #  description_long="The wrench is used to tighten the scaler tip manually.",
 #   mdn_code="Q010699",
#    sterilization = "true",
#    number_of_reuses=20,
#    base_quantity = 1,
 #   start_date="2020-02-01+01:00"
#)

push_xml = create_push_xml(
    devices_xml_list = devices,
    #service_token="YOUR_TOKEN",
    sender_actor_code="FR-AR-000014715", #CH-MF-000016224
    #sender_party_id="YOUR_PARTY_ID"
)

tree = ET.ElementTree(push_xml)
ET.indent(tree, space="    ", level=0)
tree.write(
    "eudamed_push_carbure_2.xml",
    encoding="utf-8",
    xml_declaration=True
)