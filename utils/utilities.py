from typing import Annotated,Dict,TypedDict,Literal
import operator
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate


class Cities(BaseModel):
    city1:Annotated[str,Field(description="first city of the country")]
    city2:Annotated[str,Field(description="Second city of the country")]
    date1:Annotated[list[str],Field(description="List of dates for city 1")]
    date2:Annotated[list[str],Field(description="List of dates for city 2")]

class CountryName(BaseModel):
    country_name : Annotated[str,Field(description="Name of the country")]


countries = [
    "Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan",
    "Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi",
    "Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic","Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Croatia","Cuba","Cyprus","Czechia",
    "Democratic Republic of the Congo","Denmark","Djibouti","Dominica","Dominican Republic",
    "Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia",
    "Fiji","Finland","France",
    "Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana",
    "Haiti","Honduras","Hungary",
    "Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy",
    "Jamaica","Japan","Jordan",
    "Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan",
    "Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg",
    "Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar",
    "Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Korea","North Macedonia","Norway",
    "Oman",
    "Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal",
    "Qatar",
    "Romania","Russia","Rwanda",
    "Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syria",
    "Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu",
    "Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan",
    "Vanuatu","Vatican City","Venezuela","Vietnam",
    "Yemen",
    "Zambia","Zimbabwe"
]


country_to_currency = {
    "United Arab Emirates": "AED",
    "Afghanistan": "AFN",
    "Albania": "ALL",
    "Armenia": "AMD",
    "Netherlands Antilles": "ANG",
    "Angola": "AOA",
    "Argentina": "ARS",
    "Australia": "AUD",
    "Aruba": "AWG",
    "Azerbaijan": "AZN",
    "Bosnia and Herzegovina": "BAM",
    "Barbados": "BBD",
    "Bangladesh": "BDT",
    "Bulgaria": "BGN",
    "Bahrain": "BHD",
    "Burundi": "BIF",
    "Bermuda": "BMD",
    "Brunei": "BND",
    "Bolivia": "BOB",
    "Brazil": "BRL",
    "Bahamas": "BSD",
    "Bhutan": "BTN",
    "Botswana": "BWP",
    "Belarus": "BYN",
    "Belize": "BZD",
    "Canada": "CAD",
    "Democratic Republic of the Congo": "CDF",
    "Switzerland": "CHF",
    "Chile": "CLP",
    "China": "CNY",
    "Colombia": "COP",
    "Costa Rica": "CRC",
    "Cuba": "CUP",
    "Cape Verde": "CVE",
    "Czech Republic": "CZK",
    "Djibouti": "DJF",
    "Denmark": "DKK",
    "Dominican Republic": "DOP",
    "Algeria": "DZD",
    "Egypt": "EGP",
    "Eritrea": "ERN",
    "Ethiopia": "ETB",
    "European Union": "EUR",
    "Fiji": "FJD",
    "Falkland Islands": "FKP",
    "Faroe Islands": "FOK",
    "United Kingdom": "GBP",
    "Georgia": "GEL",
    "Guernsey": "GGP",
    "Ghana": "GHS",
    "Gibraltar": "GIP",
    "The Gambia": "GMD",
    "Guinea": "GNF",
    "Guatemala": "GTQ",
    "Guyana": "GYD",
    "Hong Kong": "HKD",
    "Honduras": "HNL",
    "Croatia": "HRK",
    "Haiti": "HTG",
    "Hungary": "HUF",
    "Indonesia": "IDR",
    "Israel": "ILS",
    "Isle of Man": "IMP",
    "India": "INR",
    "Iraq": "IQD",
    "Iceland": "ISK",
    "Jersey": "JEP",
    "Jamaica": "JMD",
    "Jordan": "JOD",
    "Japan": "JPY",
    "Kenya": "KES",
    "Kyrgyzstan": "KGS",
    "Cambodia": "KHR",
    "Kiribati": "KID",
    "Comoros": "KMF",
    "South Korea": "KRW",
    "Kuwait": "KWD",
    "Cayman Islands": "KYD",
    "Kazakhstan": "KZT",
    "Laos": "LAK",
    "Lebanon": "LBP",
    "Sri Lanka": "LKR",
    "Liberia": "LRD",
    "Lesotho": "LSL",
    "Libya": "LYD",
    "Morocco": "MAD",
    "Moldova": "MDL",
    "Madagascar": "MGA",
    "North Macedonia": "MKD",
    "Myanmar": "MMK",
    "Mongolia": "MNT",
    "Macau": "MOP",
    "Mauritania": "MRU",
    "Mauritius": "MUR",
    "Maldives": "MVR",
    "Malawi": "MWK",
    "Mexico": "MXN",
    "Malaysia": "MYR",
    "Mozambique": "MZN",
    "Namibia": "NAD",
    "Nigeria": "NGN",
    "Nicaragua": "NIO",
    "Norway": "NOK",
    "Nepal": "NPR",
    "New Zealand": "NZD",
    "Oman": "OMR",
    "Panama": "PAB",
    "Peru": "PEN",
    "Papua New Guinea": "PGK",
    "Philippines": "PHP",
    "Pakistan": "PKR",
    "Poland": "PLN",
    "Paraguay": "PYG",
    "Qatar": "QAR",
    "Romania": "RON",
    "Serbia": "RSD",
    "Russia": "RUB",
    "Rwanda": "RWF",
    "Saudi Arabia": "SAR",
    "Solomon Islands": "SBD",
    "Seychelles": "SCR",
    "Sudan": "SDG",
    "Sweden": "SEK",
    "Singapore": "SGD",
    "Saint Helena": "SHP",
    "Sierra Leone": "SLE",
    "Somalia": "SOS",
    "Suriname": "SRD",
    "South Sudan": "SSP",
    "São Tomé and Príncipe": "STN",
    "Syria": "SYP",
    "Eswatini": "SZL",
    "Thailand": "THB",
    "Tajikistan": "TJS",
    "Turkmenistan": "TMT",
    "Tunisia": "TND",
    "Tonga": "TOP",
    "Turkey": "TRY",
    "Trinidad and Tobago": "TTD",
    "Tuvalu": "TVD",
    "Taiwan": "TWD",
    "Tanzania": "TZS",
    "Ukraine": "UAH",
    "Uganda": "UGX",
    "United States": "USD",
    "Uruguay": "UYU",
    "Uzbekistan": "UZS",
    "Venezuela": "VES",
    "Vietnam": "VND",
    "Vanuatu": "VUV",
    "Samoa": "WST",
    "CEMAC": "XAF",
    "Organisation of Eastern Caribbean States": "XCD",
    "International Monetary Fund": "XDR",
    "CFA": "XOF",
    "Collectivités d'Outre-Mer": "XPF",
    "Yemen": "YER",
    "South Africa": "ZAR",
    "Zambia": "ZMW",
    "Zimbabwe": "ZWL"
}


class BudgetBreakdown(BaseModel):
    total: Annotated[float, Field(description="Total budget of the trip")]
    accommodation: Annotated[float, Field(description="Total Expense on Accomodation")]
    food: Annotated[float, Field(description="Total Expense on Food")]
    transport: Annotated[float, Field(description="Total Expense on transport")]
    activities: Annotated[float, Field(description="Total Expense on activities")]
    misc: Annotated[float, Field(description="Miscellaneous expenses on the trip")]

class WeatherTemp(BaseModel):
    max_temp_c:Annotated[float,Field(description="Maximum temperature of the day")]
    min_temp_c:Annotated[float,Field(description="Minimum temperature of the day")]

class Morning(BaseModel):
    acitivity: Annotated[str,Field(description="Activity to be conduted in the morning on the respective day")]
    description: Annotated[str,Field(description="Description of the activity")]
    rating: Annotated[float,Field(description="Rating of the activity")]

class Afternoon(BaseModel):
    acitivity: Annotated[str,Field(description="Activity to be conduted in the afternoon on the respective day")]
    description: Annotated[str,Field(description="Description of the activity")]
    rating: Annotated[float,Field(description="Rating of the activity")]

class Evening(BaseModel):
    restaurant: Annotated[str,Field(description="Restaurent to be visited in the evening")]
    description: Annotated[str,Field(description="Description of the restaurent")]
    rating: Annotated[float,Field(description="Rating of the restaurent")]

class DayItinerary(BaseModel):
    day: Annotated[int, Field(description="Day number of the trip",examples=["Day 1","Day 2"])]
    date: Annotated[str,Field(description="The date of the day of the trip in YYYY-mm-dd format",examples=["2026-04-28","2026-04-29"])]
    city: Annotated[str,Field(description="Name of the city to be visited on the respective day")]
    weather: Annotated[WeatherTemp,Field(description="Stores maximum and minimum temperature of the respective day")]
    morning: Annotated[Morning,Field(description="activity to be conducted in the morning along with its description")]
    afternoon: Annotated[Morning,Field(description="activity to be conducted in the afternoon along with its description")]
    evening: Annotated[Morning,Field(description="Restaurents to be visited in the evening along with its description")]

class ModesTransport(BaseModel):
    city: Annotated[str,Field(description="Name of the city")]
    modes_of_transportation: Annotated[list[str],Field(description="List of modes of the transporation for the city")]

class Itinerary(BaseModel):
    destination_overview: Annotated[str, Field(description="Short 2-3 lines description of the location, with currency description if location is not India")]
    total_days: Annotated[int,Field(description="Total number of days for the trip")]
    budget: Annotated[BudgetBreakdown,Field(description="Breakdown of the budget for the trip")]
    itinerary: Annotated[list[DayItinerary],Field(description="List of complete itinerary of all the days")]
    transporatation: Annotated[ModesTransport,Field(description="Contains city name and modes of transporation in that city")]
    conluding_remarks: Annotated[str, Field(description="An ending statement to excite user for the trip")]
