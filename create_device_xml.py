import xml.etree.ElementTree as ET

def create_device_xml(
    risk_class,
    model,
    name,
    primary_DI,
    manufacturer_code,
    basic_UDIDI,
    reference,
    trade_name,
    description,
    mdn_code,
    sterilization,
    number_of_reuses,
    reusable,
    diameter,
    length,
    #packaging_DI,
    number_of_items,
    start_date="2020-02-01+01:00"
):

    Device = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/v1"
    XSI = "http://www.w3.org/2001/XMLSchema-instance"
    Basicudi = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/BasicUDI/v1"
    Udidi = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/UDIDI/v1"
    Commondi = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/CommonDevice/v1"
    Marketinfo = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/MktInfo/MarketInfo/v1"
    Lsn ="https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Common/LanguageSpecific/v1"
    Links = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Links/v1"

    device = ET.Element(
    f"{{{Device}}}Device",
    {f"{{{XSI}}}type": "device:MDRDeviceType"}
    )

    # -------------------------
    # MDRBasicUDI
    # -------------------------
    basic = ET.SubElement(device, f"{{{Device}}}MDRBasicUDI")

    ET.SubElement(basic, f"{{{Basicudi}}}riskClass").text = risk_class

    modelET = ET.SubElement(basic, f"{{{Basicudi}}}modelName")
    #ET.SubElement(model, f"{{{Basicudi}}}model").text = description_short
    ET.SubElement(modelET, f"{{{Commondi}}}model").text = model
    ET.SubElement(modelET, f"{{{Commondi}}}name").text = name

    identifier = ET.SubElement(basic, f"{{{Basicudi}}}identifier")
    ET.SubElement(identifier, f"{{{Commondi}}}DICode").text = primary_DI
    ET.SubElement(identifier, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    ET.SubElement(basic, f"{{{Basicudi}}}animalTissuesCells").text = "false"
    ET.SubElement(basic, f"{{{Basicudi}}}humanTissuesCells").text = "false"
    ET.SubElement(basic, f"{{{Basicudi}}}MFActorCode").text = manufacturer_code
    ET.SubElement(basic, f"{{{Basicudi}}}humanProductCheck").text = "false"
    ET.SubElement(basic, f"{{{Basicudi}}}IIb_implantable_exceptions").text = "false"
    ET.SubElement(basic, f"{{{Basicudi}}}medicinalProductCheck").text = "false"
    #ET.SubElement(basic, f"{{{Basicudi}}}specialDevice").text  not needed
    ET.SubElement(basic, f"{{{Basicudi}}}type").text = "DEVICE"
    
    #ET.SubElement(basic, f"{{{Commondi}}}type").text = "DEVICE"
    ET.SubElement(basic, f"{{{Commondi}}}active").text = "false"
    ET.SubElement(basic, f"{{{Commondi}}}administeringMedicine").text = "false"
    ET.SubElement(basic, f"{{{Commondi}}}implantable").text = "false"
    ET.SubElement(basic, f"{{{Commondi}}}measuringFunction").text = "false"
    ET.SubElement(basic, f"{{{Commondi}}}reusable").text = reusable
    
    # -------------------------
    # MDRUDIDIData
    # -------------------------
    udidi = ET.SubElement(device, f"{{{Device}}}MDRUDIDIData")

    identifier2 = ET.SubElement(udidi, f"{{{Udidi}}}identifier")
    ET.SubElement(identifier2, f"{{{Commondi}}}DICode").text = basic_UDIDI
    ET.SubElement(identifier2, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    status = ET.SubElement(udidi, f"{{{Udidi}}}status")
    ET.SubElement(status, f"{{{Commondi}}}code").text = "ON_THE_MARKET"

    desc = ET.SubElement(udidi, f"{{{Udidi}}}additionalDescription")
    name_block = ET.SubElement(desc, f"{{{Lsn}}}name")

    ET.SubElement(name_block, f"{{{Lsn}}}language").text = "EN"
    ET.SubElement(name_block, f"{{{Lsn}}}textValue").text = description

    basicUDI = ET.SubElement(udidi, f"{{{Udidi}}}basicUDIIdentifier")
    ET.SubElement(basicUDI, f"{{{Commondi}}}DICode").text = primary_DI
    ET.SubElement(basicUDI, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    ET.SubElement(udidi, f"{{{Udidi}}}MDNCodes").text = mdn_code
    ET.SubElement(udidi, f"{{{Udidi}}}productionIdentifier").text = "BATCH_NUMBER MANUFACTURING_DATE"
    ET.SubElement(udidi, f"{{{Udidi}}}referenceNumber").text = reference
    ET.SubElement(udidi, f"{{{Udidi}}}sterile").text = "false"
    ET.SubElement(udidi, f"{{{Udidi}}}sterilization").text = sterilization

    trade = ET.SubElement(udidi, f"{{{Udidi}}}tradeNames")
    trade_name_block = ET.SubElement(trade, f"{{{Lsn}}}name")

    #packages = ET.SubElement(udidi, f"{{{Udidi}}}packages")
    #package = ET.SubElement(packages, f"{{{Udidi}}}package")

    # identifier
    #identifier = ET.SubElement(package, f"{{{Udidi}}}identifier")
    #ET.SubElement(identifier, f"{{{Commondi}}}DICode").text = packaging_DI
    #ET.SubElement(identifier, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    # status
    #status = ET.SubElement(package, f"{{{Udidi}}}status")
    #ET.SubElement(status, f"{{{Commondi}}}code").text = "ON_THE_MARKET"

    # child
    #child = ET.SubElement(package, f"{{{Udidi}}}child")
    #ET.SubElement(child, f"{{{Commondi}}}DICode").text = primary_DI
    #ET.SubElement(child, f"{{{Commondi}}}issuingEntityCode").text = "GS1"

    # number of items
    #ET.SubElement(package, f"{{{Udidi}}}numberOfItems").text = number_of_items

    ET.SubElement(trade_name_block, f"{{{Lsn}}}language").text = "EN"
    ET.SubElement(trade_name_block, f"{{{Lsn}}}textValue").text = trade_name

    ET.SubElement(
        udidi,
        f"{{{Udidi}}}numberOfReuses"
    ).text = str(number_of_reuses)

    # -------------------------
    # Market Infos
    # -------------------------
    market_infos = ET.SubElement(
        udidi,
        f"{{{Udidi}}}marketInfos"
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
            f"{{{Marketinfo}}}marketInfo"
        )

        ET.SubElement(
            mi,
            f"{{{Marketinfo}}}country"
        ).text = c

        ET.SubElement(
            mi,
            f"{{{Marketinfo}}}originalPlacedOnTheMarket"
        ).text = "true" if c == "FR" else "false"

        ET.SubElement(
            mi,
            f"{{{Marketinfo}}}startDate"
        ).text = start_date
    ET.SubElement(udidi, f"{{{Udidi}}}baseQuantity").text = number_of_items
    ET.SubElement(udidi, f"{{{Udidi}}}latex").text = "false"
    ET.SubElement(udidi, f"{{{Udidi}}}reprocessed").text = "false"

    clinical_sizes = ET.SubElement(udidi, f"{{{Udidi}}}clinicalSizes")

    # -------------------
    # Diameter
    # -------------------
    cs1 = ET.SubElement(
        clinical_sizes,
        f"{{{Commondi}}}clinicalSize",
        {f"{{{XSI}}}type": "commondi:ValueClinicalSizeType"}
    )

    ET.SubElement(cs1, f"{{{Commondi}}}clinicalSizeType").text = "CST9"
    ET.SubElement(cs1, f"{{{Commondi}}}value").text = str(diameter)
    ET.SubElement(cs1, f"{{{Commondi}}}valueUnit").text = "MU50"

    # -------------------
    # Length
    # -------------------
    cs2 = ET.SubElement(
        clinical_sizes,
        f"{{{Commondi}}}clinicalSize",
        {f"{{{XSI}}}type": "commondi:ValueClinicalSizeType"}
    )

    ET.SubElement(cs2, f"{{{Commondi}}}clinicalSizeType").text = "CST19"
    ET.SubElement(cs2, f"{{{Commondi}}}value").text = str(length)
    ET.SubElement(cs2, f"{{{Commondi}}}valueUnit").text = "MU50"

    return device