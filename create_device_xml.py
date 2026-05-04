import xml.etree.ElementTree as ET

def create_device_xml(
    risk_class,
    description_short,
    primary_DI,
    basic_UDIDI,
    reference,
    trade_name,
    description_long,
    mdn_code,
    sterilization,
    number_of_reuses,
    base_quantity,
    start_date="2020-02-01+01:00"
):

    device = ET.Element(
        "device:Device",
        {"xsi:type": "device:MDRDeviceType"}
    )

    # -------------------------
    # MDRBasicUDI
    # -------------------------
    basic = ET.SubElement(device, "device:MDRBasicUDI")

    ET.SubElement(basic, "basicudi:riskClass").text = risk_class

    model = ET.SubElement(basic, "basicudi:modelName")
    #ET.SubElement(model, "basicudi:model").text = description_short
    ET.SubElement(model, "commondi:model").text = description_short
    ET.SubElement(model, "commondi:name").text = description_short

    identifier = ET.SubElement(basic, "basicudi:identifier")
    ET.SubElement(identifier, "commondi:DICode").text = primary_DI
    ET.SubElement(identifier, "commondi:issuingEntityCode").text = "GS1"

    ET.SubElement(basic, "basicudi:animalTissuesCells").text = "false"
    ET.SubElement(basic, "basicudi:humanTissuesCells").text = "false"
    ET.SubElement(basic, "basicudi:MFActorCode").text = "BE-MF-000000002"
    ET.SubElement(basic, "basicudi:humanProductCheck").text = "false"
    ET.SubElement(basic, "basicudi:IIb_implantable_exceptions").text = "false"
    ET.SubElement(basic, "basicudi:medicinalProductCheck").text = "false"
    #ET.SubElement(basic, "basicudi:specialDevice").text  not needed
    ET.SubElement(basic, "basicudi:type").text = "DEVICE"
    
    #ET.SubElement(basic, "commondi:type").text = "DEVICE"
    ET.SubElement(basic, "commondi:active").text = "false"
    ET.SubElement(basic, "commondi:administeringMedicine").text = "false"
    ET.SubElement(basic, "commondi:implantable").text = "false"
    ET.SubElement(basic, "commondi:measuringFunction").text = "false"
    ET.SubElement(basic, "commondi:reusable").text = "false"
    
    # -------------------------
    # MDRUDIDIData
    # -------------------------
    udidi = ET.SubElement(device, "device:MDRUDIDIData")

    identifier2 = ET.SubElement(udidi, "udidi:identifier")
    ET.SubElement(identifier2, "commondi:DICode").text = basic_UDIDI
    ET.SubElement(identifier2, "commondi:issuingEntityCode").text = "GS1"

    status = ET.SubElement(udidi, "udidi:status")
    ET.SubElement(status, "commondi:code").text = "ON_THE_MARKET"

    desc = ET.SubElement(udidi, "udidi:additionalDescription")
    name_block = ET.SubElement(desc, "lsn:name")

    ET.SubElement(name_block, "lsn:language").text = "EN"
    ET.SubElement(name_block, "lsn:textValue").text = description_long

    basicUDI = ET.SubElement(udidi, "udidi:basicUDIIdentifier")
    ET.SubElement(basicUDI, "commondi:DICode").text = primary_DI
    ET.SubElement(basicUDI, "commondi:issuingEntityCode").text = "GS1"

    ET.SubElement(udidi, "udidi:MDNCodes").text = mdn_code
    ET.SubElement(udidi, "udidi:productionIdentifier").text = "BATCH_NUMBER MANUFACTURING_DATE"
    ET.SubElement(udidi, "udidi:referenceNumber").text = reference
    ET.SubElement(udidi, "udidi:sterile").text = "false"
    ET.SubElement(udidi, "udidi:sterilization").text = sterilization

    trade = ET.SubElement(udidi, "udidi:tradeNames")
    trade_name_block = ET.SubElement(trade, "lsn:name")

    ET.SubElement(trade_name_block, "lsn:language").text = "EN"
    ET.SubElement(trade_name_block, "lsn:textValue").text = trade_name

    #packages TODO add package management 
    ET.SubElement(
        udidi,
        "udidi:numberOfReuses"
    ).text = str(number_of_reuses)

    # -------------------------
    # Market Infos
    # -------------------------
    market_infos = ET.SubElement(
        udidi,
        "udidi:marketInfos"
    )

    countries = [
        "AT","BE","BG","HR","CY","CZ","DK",
        "EE","FI","FR","DE","EL","HU","IS",
        "IE","IT","LV","LI","LT","LU","MT",
        "PT","NL","NO","PL","RO","SK","SI",
        "ES","SE","TR","XI"
    ]

    for c in countries:

        mi = ET.SubElement(
            market_infos,
            "marketinfo:marketInfo"
        )

        ET.SubElement(
            mi,
            "marketinfo:country"
        ).text = c

        ET.SubElement(
            mi,
            "marketinfo:originalPlacedOnTheMarket"
        ).text = "true" if c == "FR" else "false"

        ET.SubElement(
            mi,
            "marketinfo:startDate"
        ).text = start_date
    ET.SubElement(udidi, "udidi:baseQuantity").text = str(base_quantity)
    ET.SubElement(udidi, "udidi:latex").text = "false"
    ET.SubElement(udidi, "udidi:reprocessed").text = "false"

    return device