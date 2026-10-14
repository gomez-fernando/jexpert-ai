# Catálogo de atributos

Extraído el 2026-10-14 de la sandbox `dev` con `scripts/extract_catalog.py`, sobre los datasets cuyo nombre casa con `^fdg_tfm_bbank_`.

La base de clientes es `fdg_tfm_bbank_profiledata`, con 7.730 clientes identificados por `personID` en el namespace `TRBbankProfileID`. La cobertura por clientes se calcula sobre esa base.

## Datasets

| Dataset | Clase | Filas | Clientes | Ventana de datos | Última carga | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `fdg_tfm_bbank_applications` | evento | 40.414 | 7.354 | 2025-10-01 a 2026-06-28 | 2026-10-14 |  |
| `fdg_tfm_bbank_atminfo` | tabla de apoyo | 43 |  |  | 2026-10-14 |  |
| `fdg_tfm_bbank_atmtransactions` | evento | 1.000 | 321 | 2006-02-06 a 2024-05-24 | 2026-10-14 |  |
| `fdg_tfm_bbank_bankaccount` | perfil | 2.530 | 2.530 |  | 2026-10-14 |  |
| `fdg_tfm_bbank_branch` | tabla de apoyo | 11 |  |  | 2026-10-10 |  |
| `fdg_tfm_bbank_fulfillment` | evento | 15.577 | 7.640 | 2025-10-04 a 2026-07-01 | 2026-10-14 |  |
| `fdg_tfm_bbank_loyalty` | perfil | 1.002 | 502 |  | 2026-10-14 | 500 de sus 502 clientes aparecen en dos filas con los mismos puntos, así que hay que contar clientes y no filas. |
| `fdg_tfm_bbank_productinteractions` | evento | 315 | 55 | 2018-11-12 a 2025-05-27 | 2026-10-14 |  |
| `fdg_tfm_bbank_products` | tabla de apoyo | 44 |  |  | 2026-10-14 |  |
| `fdg_tfm_bbank_profiledata` | perfil | 7.730 | 7.730 |  | 2026-10-14 |  |
| `fdg_tfm_bbank_propensity` | perfil | 100 |  |  | 2026-10-14 | No cruza con ningún cliente de la base: ninguno de sus emails está en fdg_tfm_bbank_profiledata. |
| `fdg_tfm_bbank_webinteractions` | evento | 260.627 | 6.782 | 2025-10-01 a 2026-06-28 | 2026-10-14 |  |

## Cruces entre datasets

| Origen | Campo | Destino | Campo de destino | Valores | Encontrados |
| --- | --- | --- | --- | --- | --- |
| `fdg_tfm_bbank_applications` | `_valuelabemeaptrsd.ApplicationDetails.profileID` | `fdg_tfm_bbank_profiledata` | `personID` | 7.354 | 7.354 (100,0 %) |
| `fdg_tfm_bbank_atmtransactions` | `_valuelabemeaptrsd.transactionIdentifiers.profileId` | `fdg_tfm_bbank_profiledata` | `personID` | 321 | 321 (100,0 %) |
| `fdg_tfm_bbank_bankaccount` | `personID` | `fdg_tfm_bbank_profiledata` | `personID` | 2.530 | 2.525 (99,8 %) |
| `fdg_tfm_bbank_fulfillment` | `_valuelabemeaptrsd.DetailsOfFulfillment.profileID_` | `fdg_tfm_bbank_profiledata` | `personID` | 7.640 | 7.640 (100,0 %) |
| `fdg_tfm_bbank_loyalty` | `personID` | `fdg_tfm_bbank_profiledata` | `personID` | 502 | 500 (99,6 %) |
| `fdg_tfm_bbank_productinteractions` | `_valuelabemeaptrsd.transactionIdentifiers.profileId` | `fdg_tfm_bbank_profiledata` | `personID` | 55 | 55 (100,0 %) |
| `fdg_tfm_bbank_propensity` | `_valuelabemeaptrsd.email` | `fdg_tfm_bbank_profiledata` | `personalEmail.address` | 100 | 0 (0,0 %) |
| `fdg_tfm_bbank_webinteractions` | `_valuelabemeaptrsd.transaction_identifiers.profile_id` | `fdg_tfm_bbank_profiledata` | `personID` | 6.782 | 6.782 (100,0 %) |
| `fdg_tfm_bbank_applications` | `_valuelabemeaptrsd.ApplicationDetails.Email` | `fdg_tfm_bbank_profiledata` | `personalEmail.address` | 23.950 | 7.714 (32,2 %) |
| `fdg_tfm_bbank_propensity` | `personalEmail.address` | `fdg_tfm_bbank_profiledata` | `personalEmail.address` | 100 | 0 (0,0 %) |
| `fdg_tfm_bbank_webinteractions` | `_valuelabemeaptrsd.transaction_identifiers.emailAddress` | `fdg_tfm_bbank_profiledata` | `personalEmail.address` | 27.326 | 7.727 (28,3 %) |
| `fdg_tfm_bbank_atmtransactions` | `_valuelabemeaptrsd.transactionIdentifiers.atmId` | `fdg_tfm_bbank_atminfo` | `atmID` | 37 | 37 (100,0 %) |
| `fdg_tfm_bbank_atmtransactions` | `_valuelabemeaptrsd.transactionData.transactionType` | `fdg_tfm_bbank_productinteractions` | `_valuelabemeaptrsd.transactionIdentifiers.profileId` | 4 | 0 (0,0 %) |
| `fdg_tfm_bbank_fulfillment` | `_valuelabemeaptrsd.DetailsOfFulfillment.applicationID` | `fdg_tfm_bbank_applications` | `_valuelabemeaptrsd.ApplicationDetails.Application.applicationID` | 10.528 | 10.528 (100,0 %) |
| `fdg_tfm_bbank_fulfillment` | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.branchID_` | `fdg_tfm_bbank_branch` | `branchID` | 5 | 5 (100,0 %) |
| `fdg_tfm_bbank_productinteractions` | `_valuelabemeaptrsd.transactionIdentifiers.productId` | `fdg_tfm_bbank_products` | `productID` | 36 | 36 (100,0 %) |
| `fdg_tfm_bbank_profiledata` | `_valuelabemeaptrsd.financialDetail.branch_id` | `fdg_tfm_bbank_branch` | `branchID` | 13 | 9 (69,2 %) |
| `fdg_tfm_bbank_webinteractions` | `_valuelabemeaptrsd.transaction_identifiers.product_id` | `fdg_tfm_bbank_products` | `productID` | 5 | 5 (100,0 %) |
| `fdg_tfm_bbank_webinteractions` | `_valuelabemeaptrsd.transaction_identifiers.applicationID` | `fdg_tfm_bbank_applications` | `_valuelabemeaptrsd.ApplicationDetails.Application.applicationID` | 40.414 | 40.414 (100,0 %) |

## Atributos de `fdg_tfm_bbank_applications`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| profileID | `_valuelabemeaptrsd.ApplicationDetails.profileID` | identificador de cliente | 26,1 % | 95,1 % | 7.354 valores distintos, que no se muestran | Solicitud denegada: ninguna de las denegadas lleva profileID. Las denegadas solo se pueden atribuir a un cliente cruzando _valuelabemeaptrsd.ApplicationDetails.Email con personalEmail.address de fdg_tfm_bbank_profiledata. El 2026-10-14, ese cruce daba 2.958 clientes de la base con alguna solicitud denegada. |
| Email | `_valuelabemeaptrsd.ApplicationDetails.Email` | dato personal | 100,0 % | 95,1 % | 23.950 valores distintos, que no se muestran |  |
| EmailHash | `_valuelabemeaptrsd.ApplicationDetails.EmailHash` | identificador | 100,0 % | 95,1 % | 23.950 valores distintos, que no se muestran |  |
| rejectionReason | `_valuelabemeaptrsd.ApplicationDetails.Application.rejectionReason` | atributo | 73,9 % | 0,0 % | high_risk 10.015, fraud_suspected 9.973, incomplete_application 9.898 | Solicitud aceptada: las aceptadas no llevan motivo de rechazo. Como las denegadas no llevan profileID, su cobertura en clientes sale a 0. Para saber qué clientes tienen una solicitud denegada hay que cruzar por email (ver la nota de profileID). |
| finalStatus | `_valuelabemeaptrsd.ApplicationDetails.Application.finalStatus` | atributo | 100,0 % | 95,1 % | denied 29.886, accepted 10.528 |  |
| applicationID | `_valuelabemeaptrsd.ApplicationDetails.Application.applicationID` | identificador | 100,0 % | 95,1 % | 40.414 valores distintos, que no se muestran |  |
| productID | `_valuelabemeaptrsd.ApplicationDetails.productID` | atributo | 100,0 % | 95,1 % | 597-824-395766967583 16.436, 117-092-615581165598 16.288, 590-882-735839612672 2.586, 816-504-258387688508 2.578, 102-349-853011058806 2.526 | 597-824-395766967583 es Premium Account y 117-092-615581165598 es Standard Account (cuentas de ahorro). 590-882-735839612672 es Bbank Customized Cash Rewards, 816-504-258387688508 es Bbank Green Card y 102-349-853011058806 es Bbank Premium Card (tarjetas de crédito). Los nombres están en fdg_tfm_bbank_products. |
| Timestamp | `timestamp` | fecha del evento | 100,0 % | 95,1 % | De 2025-10-01 a 2026-06-28 |  |

## Atributos de `fdg_tfm_bbank_atminfo`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Branch ID | `_valuelabemeaptrsd.branch_id` | atributo | 100,0 % |  | BIL01 5, LIS01 5, MAD01 5, SEV01 5, VAL01 5, ROM01 4, OVI01 4, BAR01 4, MIL01 3, OPO01 3 |  |
| City | `atmAddress.city` | atributo | 100,0 % |  | Lisboa 5, Valencia 5, Bilbao 5, Sevilla 5, Madrid 5, Rome 4, Oviedo 4, Barcelona 4, Milan 3, Oporto 3 |  |
| ATM ID | `atmID` | identificador | 100,0 % |  | 43 valores distintos, que no se muestran |  |
| Is ATM Active | `isAtmActive` | atributo | 100,0 % |  | true 38, false 5 |  |

## Atributos de `fdg_tfm_bbank_atmtransactions`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| ATM ID | `_valuelabemeaptrsd.transactionIdentifiers.atmId` | atributo | 100,0 % | 4,2 % | 37 valores distintos |  |
| Profile ID | `_valuelabemeaptrsd.transactionIdentifiers.profileId` | identificador de cliente | 100,0 % | 4,2 % | 321 valores distintos, que no se muestran |  |
| Transaction Type | `_valuelabemeaptrsd.transactionData.transactionType` | atributo | 100,0 % | 4,2 % | cash_withdrawal 341, cash_deposit 243, money_transfer 218, bill_payment 198 |  |
| Amount | `_valuelabemeaptrsd.transactionData.amount` | atributo | 100,0 % | 4,2 % | De 52,22 a 3.000, mediana 1.550,73 |  |
| Timestamp | `timestamp` | fecha del evento | 100,0 % | 4,2 % | De 2006-02-06 a 2024-05-24 |  |

## Atributos de `fdg_tfm_bbank_bankaccount`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Account Type | `_valuelabemeaptrsd.BankAccountDetails.accountType` | atributo | 100,0 % | 32,7 % | Checking 1.824, Savings 706 |  |
| Account Balance | `_valuelabemeaptrsd.BankAccountDetails.accountBalance` | atributo | 100,0 % | 32,7 % | De -611,17 a 87.324, mediana 13.425,30 | Saldo en el momento de la carga, sin histórico. |
| Is Active | `_valuelabemeaptrsd.BankAccountDetails.isActive` | atributo | 100,0 % | 32,7 % | true 2.521, false 9 |  |
| IBAN | `_valuelabemeaptrsd.financialDetail.iban` | dato personal | 100,0 % | 32,7 % | 2.446 valores distintos, que no se muestran |  |
| Person ID | `personID` | identificador de cliente | 100,0 % | 32,7 % | 2.530 valores distintos, que no se muestran |  |

## Atributos de `fdg_tfm_bbank_branch`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| City | `branchAddress.city` | atributo | 100,0 % |  | Valencia 1, Rome 1, Oviedo 1, Bilbao 1, Milan 1, Porto 1, Sevilla 1, Madrid 1, Lisbon 1, Toledo 1, Barcelona 1 |  |
| Postal code | `branchAddress.postalCode` | atributo | 100,0 % |  | 1100-473 1, 48015 1, 20122  1, 00152 1, 45071 1, 28012 1, 08915 1, 33008 1, 41004 1, 4300-059 1, 46002 1 |  |
| Street 1 | `branchAddress.street1` | atributo | 100,0 % |  | Via Giambattista Marino 1, Campo de Santa Clara 113 1, Corso di Porta Romana 15 1, Calle de les Barques, 10 1, Avenida. de la Constitución, 3 1, Plaza del Consistorio 1 1, Calle Pedro I Pons, 1 1, Calle Eusebio Garcia Alonso 3 1, Rua de Gomes Freire 198 1, Plaza del Angel, 12 1, Calle Campomanes 11 1 |  |
| Street 2 | `branchAddress.street2` | atributo | 100,0 % |  | Casco Antiguo 2, Barrio Salamanca 1, Centro Storico 1, Centro 1, Chamartin 1, Ciutat Vella 1, Bonfim 1, Torrino 1, Santo António 1, Sant Cugat del Valles 1 |  |
| Branch ID | `branchID` | identificador | 100,0 % |  | 11 valores distintos, que no se muestran |  |

## Atributos de `fdg_tfm_bbank_fulfillment`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| deliveryStatus_ | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.deliveryStatus_` | atributo | 100,0 % | 98,8 % | delivered 7.812, pending 7.765 |  |
| fulfillmentMethod_ | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.fulfillmentMethod_` | atributo | 100,0 % | 98,8 % | home 7.907, branch 7.670 |  |
| branchID_ | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.branchID_` | atributo | 49,2 % | 61,7 % | BAR01 1.663, BIL01 1.651, MAD01 1.641, SEV01 1.606, VAL01 1.109 | Entrega a domicilio, sin sucursal. |
| applicationID | `_valuelabemeaptrsd.DetailsOfFulfillment.applicationID` | atributo | 67,6 % | 95,1 % | 10.528 valores distintos |  |
| profileID_ | `_valuelabemeaptrsd.DetailsOfFulfillment.profileID_` | identificador de cliente | 100,0 % | 98,8 % | 7.640 valores distintos, que no se muestran |  |
| fulfillmentID | `eventMergeId` | identificador | 100,0 % | 98,8 % | 15.577 valores distintos, que no se muestran |  |
| Timestamp | `timestamp` | fecha del evento | 100,0 % | 98,8 % | De 2025-10-04 a 2026-07-01 |  |

## Atributos de `fdg_tfm_bbank_loyalty`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Program Join Date | `loyalty.joinDate` | atributo | 100,0 % | 6,5 % | De 2005-05-30 a 2025-07-16 |  |
| Program Points Balance | `loyalty.points` | atributo | 100,0 % | 6,5 % | De 1 a 998, mediana 491 |  |
| Person ID | `personID` | identificador de cliente | 100,0 % | 6,5 % | 502 valores distintos, que no se muestran |  |

## Atributos de `fdg_tfm_bbank_productinteractions`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Transaction Type | `_valuelabemeaptrsd.transactionData.transactionType` | atributo | 98,4 % | 0,7 % | purchase 88, interest 80, inquiries 70, renewal 68, addToCart 3, favourite 1 |  |
| Product ID | `_valuelabemeaptrsd.transactionIdentifiers.productId` | atributo | 100,0 % | 0,7 % | 36 valores distintos |  |
| Profile ID | `_valuelabemeaptrsd.transactionIdentifiers.profileId` | identificador de cliente | 100,0 % | 0,7 % | 55 valores distintos, que no se muestran |  |
| Event Type | `eventType` | atributo | 49,2 % | 0,7 % | purchase 46, interest 40, inquiries 35, renewal 34 |  |
| Timestamp | `timestamp` | fecha del evento | 100,0 % | 0,7 % | De 2018-11-12 a 2025-05-27 |  |

## Atributos de `fdg_tfm_bbank_products`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Product Category Name | `productCategoryName` | atributo | 97,7 % |  | Credit Card 11, Savings Account 8, Personal Loan 6, Investment Account 6, Mortgage 6, Checking Account 6 |  |
| Product ID | `productID` | identificador | 100,0 % |  | 44 valores distintos, que no se muestran |  |
| Product Name | `productName` | atributo | 97,7 % |  | 43 valores distintos |  |

## Atributos de `fdg_tfm_bbank_profiledata`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Branch ID | `_valuelabemeaptrsd.financialDetail.branch_id` | atributo | 100,0 % | 100,0 % | BIL01 1.372, MAD01 1.367, SEV01 1.331, BAR01 1.330, VAL01 1.068, OVI01 323, ZAR01 272, VLC01 254, MAL01 252, MIL01 49, OPO01 41, LIS01 39, … | ZAR01, VLC01, MAL01 y OPO01 no tienen ficha en fdg_tfm_bbank_branch. |
| Annual Income | `_valuelabemeaptrsd.financialDetail.annualIncome` | atributo | 100,0 % | 100,0 % | De 11.110 a 79.991, mediana 42.791 |  |
| Product IDs | `_valuelabemeaptrsd.financialDetail.product_ids[]` | atributo | 100,0 % | 100,0 % | 527 valores distintos | Cada lista llega como un único texto (['597-824-395766967583']), así que no se puede filtrar por producto sin tratarla antes. |
| Preapproved Credit Amount | `_valuelabemeaptrsd.financialDetail.preapprovedCreditAmount` | atributo | 100,0 % | 100,0 % | De 1.501 a 36.300, mediana 14.238 |  |
| First Product Activation Date | `_valuelabemeaptrsd.financialDetail.firstProductActivationDate` | atributo | 100,0 % | 100,0 % | De 2005-01-19 a 2026-06-28 |  |
| IBAN | `_valuelabemeaptrsd.financialDetail.iban` | dato personal | 100,0 % | 100,0 % | 7.646 valores distintos, que no se muestran |  |
| DNI | `_valuelabemeaptrsd.Identifiers.identityNumber` | dato personal | 100,0 % | 100,0 % | 7.730 valores distintos, que no se muestran |  |
| Person ID | `personID` | identificador de cliente | 100,0 % | 100,0 % | 7.730 valores distintos, que no se muestran |  |
| Address | `personalEmail.address` | identificador | 100,0 % | 100,0 % | 7.730 valores distintos, que no se muestran |  |
| City | `homeAddress.city` | atributo | 100,0 % | 100,0 % | Bilbao 1.372, Madrid 1.367, Sevilla 1.331, Barcelona 1.330, Valencia 1.068, Oviedo 323, Zaragoza 272, València 254, Málaga 252, Milan 49, Oporto 41, Lisboa 39, … | Valencia y València son valores distintos, así que hay que sumar los dos. |
| Postal code | `homeAddress.postalCode` | dato personal | 100,0 % | 100,0 % | 12 valores distintos, que no se muestran |  |
| Number | `mobilePhone.number` | identificador | 100,0 % | 100,0 % | 7.730 valores distintos, que no se muestran |  |
| Preferred Channel | `consents.marketing.preferred` | atributo | 100,0 % | 100,0 % | email 6.237, sms 838, push 655 |  |
| Choice Value | `consents.marketing.email.val` | atributo | 32,7 % | 32,7 % | y 1.330, n 1.195 | No hay consentimiento registrado, así que no se puede tratar como que acepta. y acepta, n rechaza. |
| Choice Value | `consents.marketing.call.val` | atributo | 32,7 % | 32,7 % | n 1.412, y 1.113 | No hay consentimiento registrado, así que no se puede tratar como que acepta. y acepta, n rechaza. |
| Birth date(YYYY-MM-DD) | `person.birthDate` | atributo | 100,0 % | 100,0 % | De 1925-04-23 a 2005-09-22 |  |
| Gender | `person.gender` | atributo | 100,0 % | 100,0 % | female 3.949, male 3.781 |  |
| First name | `person.name.firstName` | dato personal | 100,0 % | 100,0 % | 266 valores distintos, que no se muestran |  |
| Last name | `person.name.lastName` | dato personal | 100,0 % | 100,0 % | 240 valores distintos, que no se muestran |  |

## Atributos de `fdg_tfm_bbank_propensity`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| call_center_prop | `_valuelabemeaptrsd.propensity.call_center_prop` | atributo | 100,0 % |  | false 53, true 47 |  |
| cards_score | `_valuelabemeaptrsd.propensity.cards_score` | atributo | 100,0 % |  | De 3 a 99, mediana 65 |  |
| investment_score | `_valuelabemeaptrsd.propensity.investment_score` | atributo | 100,0 % |  | De 2 a 100, mediana 49 |  |
| credit_score | `_valuelabemeaptrsd.propensity.credit_score` | atributo | 100,0 % |  | De 1 a 99, mediana 61 |  |
| mortgages_score | `_valuelabemeaptrsd.propensity.mortgages_score` | atributo | 100,0 % |  | De 2 a 100, mediana 41 |  |
| email | `_valuelabemeaptrsd.email` | identificador | 100,0 % |  | 100 valores distintos, que no se muestran |  |
| jobTitle | `person._valuelabemeaptrsd.jobTitle` | atributo | 100,0 % |  | 66 valores distintos |  |
| Gender | `person.gender` | atributo | 100,0 % |  | male 53, female 47 |  |
| First name | `person.name.firstName` | dato personal | 100,0 % |  | 90 valores distintos, que no se muestran |  |
| Last name | `person.name.lastName` | dato personal | 100,0 % |  | 91 valores distintos, que no se muestran |  |
| Address | `personalEmail.address` | dato personal | 100,0 % |  | 100 valores distintos, que no se muestran |  |

## Atributos de `fdg_tfm_bbank_webinteractions`

| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Event Type | `eventType` | atributo | 100,0 % | 87,7 % | selectAccount 50.077, formAccount 45.617, conditionsaccountView 39.763, processingAccount 32.724, deniedAccount 18.940, productList 16.692, viewProduct 15.051, cartView 12.795, checkout 10.231, processingCards 7.690, confirmAccount 5.631, deniedShop 3.246, … |  |
| Timestamp | `timestamp` | fecha del evento | 100,0 % | 87,7 % | De 2025-10-01 a 2026-06-28 |  |
| Email Address | `_valuelabemeaptrsd.transaction_identifiers.emailAddress` | dato personal | 63,3 % | 87,7 % | 27.326 valores distintos, que no se muestran |  |
| Email Hasheado | `_valuelabemeaptrsd.transaction_identifiers.emailHash` | identificador | 63,3 % | 87,7 % | 27.326 valores distintos, que no se muestran |  |
| applicationID | `_valuelabemeaptrsd.transaction_identifiers.applicationID` | atributo | 27,0 % | 84,1 % | 40.414 valores distintos |  |
| Profile ID | `_valuelabemeaptrsd.transaction_identifiers.profile_id` | identificador de cliente | 28,2 % | 87,7 % | 6.782 valores distintos, que no se muestran | Evento sin cliente identificado por profile_id. Muchos de esos eventos llevan el email, que permite cruzarlos con la base (ver el cruce por email en relaciones.csv). |
| Product ID | `_valuelabemeaptrsd.transaction_identifiers.product_id` | atributo | 32,6 % | 50,5 % | 597-824-395766967583 25.156, 117-092-615581165598 24.921, 816-504-258387688508 11.753, 590-882-735839612672 11.664, 102-349-853011058806 11.572 | Los mismos códigos de producto que _valuelabemeaptrsd.ApplicationDetails.productID de fdg_tfm_bbank_applications. |
| GAID | `_valuelabemeaptrsd.GAID` | identificador | 100,0 % | 87,7 % | 50.254 valores distintos, que no se muestran |  |
| deviceType | `_valuelabemeaptrsd.Device.deviceType` | atributo | 100,0 % | 87,7 % | mobile 260.627 |  |
| URL | `_valuelabemeaptrsd.WebPageDetail.URL` | atributo | 100,0 % | 87,7 % | https://bbank.bmind.es/select-account/ 50.077, https://bbank.bmind.es/form-account/ 45.617, https://bbank.bmind.es/conditions-account/ 39.763, https://bbank.bmind.es/processing-account 32.724, https://bbank.bmind.es/denied-account/ 18.940, https://bbank.bmind.es/shop/ 16.692, https://bbank.bmind.es/product 15.051, https://bbank.bmind.es/cart/ 12.795, https://bbank.bmind.es/checkout 10.231, https://bbank.bmind.es/processing-cards 7.690, https://bbank.bmind.es/confirm-account/ 5.631, https://bbank.bmind.es/denied-shop/ 3.246, … |  |
| source | `_valuelabemeaptrsd.UTM.source` | atributo | 100,0 % | 87,7 % | google 64.429, facebook 63.271, partner 32.452, instagram 32.160, direct 31.854, affiliate 31.851, crm 4.610 |  |
| medium | `_valuelabemeaptrsd.UTM.medium` | atributo | 100,0 % | 87,7 % | cpc 96.908, organic 62.952, referral 32.452, (none) 31.854, cpa 31.851, sms 2.357, email 2.253 |  |
| campaign | `_valuelabemeaptrsd.UTM.campaign` | atributo | 100,0 % | 87,7 % | (none) 159.109, black_friday_exclusive 25.779, application_recovery_program 25.504, january_sales_finance 25.288, christmas_savings_plan 24.947 |  |
