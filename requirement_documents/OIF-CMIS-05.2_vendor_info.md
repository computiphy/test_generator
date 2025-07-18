## 8.3.2 Vendor Information

## Table 8-25 Vendor Information (Page 00h)

| Bytes   |   Length  (bytes) | Register  Name   | Register Description                                      | Type    |
|---------|-------------------|------------------|-----------------------------------------------------------|---------|
| 129-144 |                16 | VendorName       | Vendor name (ASCII)                                       | RO Rqd. |
| 145-147 |                 3 | VendorOUI        | Vendor IEEE company ID                                    | RO Rqd. |
| 148-163 |                16 | VendorPN         | Part number provided by vendor (ASCII)                    | RO Rqd. |
| 164-165 |                 2 | VendorRev        | Revision level for part number provided by vendor (ASCII) | RO Rqd. |
| 166-181 |                16 | VendorSN         | Vendor Serial Number (ASCII)                              | RO Rqd. |
| 182-189 |                 8 | DateCode         | Manufacturing Date Code (ASCII)                           | RO Rqd. |
| 190-199 |                10 | CLEICode         | Common Language Equipment Identification Code (ASCII)     | RO Rqd. |

## 8.3.2.1 Vendor Name

The VendorName is a 16 character read-only field that contains ASCII characters, left aligned and padded on the right with ASCII spaces (20h).

The VendorName shall contain the full name of the corporation, a commonly accepted abbreviation of the name of the corporation, the SCSI company code for the corporation, or the stock exchange code for the corporation. The VendorName may be the original manufacturer of the module or the name of the module reseller. In both cases, the VendorName and VendorOUI (if specified) shall correlate to the same company. At least one of the VendorName or the VendorOUI fields shall contain valid serial number manufacturing data.

## 8.3.2.2 Vendor Organizationally Unique Identifier

The  vendor  organizationally  unique  identifier  field  ( VendorOUI )  is  a  3-byte  field  that  contains  the  IEEE Company Identifier for the vendor. A value of all zero in the 3-byte field indicates that the vendor's OUI is unspecified.

## 8.3.2.3 Vendor Part Number

The vendor part number ( VendorPN ) is a 16-byte field that contains ASCII characters, left aligned and padded on the right with ASCII spaces (20h), defining the vendor part number or product name. A value of all zero in the 16-byte field indicates that the vendor part number is unspecified.

## 8.3.2.4 Vendor Revision Number

The vendor revision number ( VendorRev ) is a 2-byte field that contains ASCII characters, left aligned and padded on the right with ASCII spaces (20h), defining the vendor's product revision number. A value of all zero in the field indicates that the vendor revision number is unspecified.

## 8.3.2.5 Vendor Serial Number

The vendor serial number ( VendorSN ) is a 16-character field that contains ASCII characters, left aligned and padded on the right with ASCII spaces (20h), defining the vendor's serial number for the Prod uct. A value of all zero in the 16-byte field indicates that the vendor serial number is unspecified.

## 8.3.2.6 Date Code

The DateCode is an 8byte field that contains the vendor's date code in ASCII characters. The date code is mandatory. The date code shall be in the following format:

## Table 8-26 Date Code (Page 00h)

| Byte    | Bits   | Register Name   | Description                                   | Type    |
|---------|--------|-----------------|-----------------------------------------------|---------|
| 182-183 | All    | Year            | ASCII two low order digits of year (00=2000)  | RO Rqd. |
| 184-185 | All    | Month           | ASCII digits of month (01=Jan through 12=Dec) | RO Rqd. |
| 186-187 | All    | DayOfMonth      | ASCII day of month (01-31)                    | RO Rqd. |
| 188-189 | All    | LotCode         | ASCII custom lot code, may be blank           | RO Opt. |

## 8.3.2.7 CLEI Code

The CLEI (Common Language Equipment Identification) code is a 10byte field that contains the vendor's CLEI code in ASCII characters.

The CLEI code value is optional. If CLEI code value is not supported, a value of all ASCII 20h (spaces) shall be entered.

## Table 8-27 CLEI Code (Page 00h)

| Byte    | Bits   | Register Name   | Description                | Type    |
|---------|--------|-----------------|----------------------------|---------|
| 190-199 | All    | CLEICode        | Vendor's CLEI Code (ASCII) | RO Opt. |
