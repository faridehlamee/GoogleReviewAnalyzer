"""
Enhanced Web Interface with Better Review Display
This version shows more reviews and handles API limitations better
"""
import os
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses

# Load API key
load_dotenv()

app = Flask(__name__)

# HTML Template with better review display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Business Bad Review Finder</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 40px;
        }
        
        .form-group { 
            margin-bottom: 25px; 
        }
        
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        select { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e1e5e9; 
            border-radius: 8px; 
            font-size: 16px;
            background-color: white;
            cursor: pointer;
        }
        
        button { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 18px;
            font-weight: 600;
            width: 100%;
        }
        
        .results { 
            margin-top: 40px; 
        }
        
        .business { 
            border: 1px solid #e1e5e9; 
            padding: 20px; 
            margin-bottom: 20px; 
            border-radius: 10px;
            background: #f8f9fa;
        }
        
        .business h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .business-info {
            color: #666;
            margin-bottom: 5px;
        }
        
        .rating {
            font-weight: 600;
            color: #28a745;
        }
        
        .bad-review { 
            background-color: #fff5f5; 
            border: 1px solid #fed7d7; 
            padding: 20px; 
            margin-bottom: 15px; 
            border-radius: 10px;
            border-left: 4px solid #e53e3e;
        }
        
        .bad-review .rating { 
            color: #e53e3e; 
            font-weight: bold; 
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        
        .reviewer {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        .review-text {
            color: #555;
            line-height: 1.6;
        }
        
        .error { 
            color: #e53e3e; 
            background-color: #fed7d7; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 20px;
        }
        
        .success { 
            color: #22543d; 
            background-color: #c6f6d5; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 20px;
        }
        
        .stats {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        
        .stats h3 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .stats p {
            color: #666;
            margin-bottom: 5px;
        }
        
        .form-row {
            display: flex;
            gap: 20px;
        }
        
        .form-row .form-group {
            flex: 1;
        }
        
        .all-reviews {
            margin-top: 20px;
        }
        
        .review-item {
            border: 1px solid #e1e5e9;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            background: white;
        }
        
        .review-item.bad {
            border-left: 4px solid #e53e3e;
            background: #fff5f5;
        }
        
        .review-item.good {
            border-left: 4px solid #28a745;
            background: #f0fff4;
        }
        
        .review-rating {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .review-rating.bad {
            color: #e53e3e;
        }
        
        .review-rating.good {
            color: #28a745;
        }
        
        @media (max-width: 768px) {
            .form-row {
                flex-direction: column;
                gap: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Business Bad Review Finder</h1>
            <p>Select a business and location to find all bad reviews (less than 4 stars)</p>
        </div>
        
        <div class="content">
            <form method="POST">
                <div class="form-row">
                    <div class="form-group">
                        <label for="business_name">Business Name:</label>
                        <select id="business_name" name="business_name" required>
                            <option value="">Select a business...</option>
                            <option value="McDonald's">McDonald's</option>
                            <option value="KFC">KFC</option>
                            <option value="Burger King">Burger King</option>
                            <option value="Taco Bell">Taco Bell</option>
                            <option value="Pizza Hut">Pizza Hut</option>
                            <option value="Domino's">Domino's Pizza</option>
                            <option value="Subway">Subway</option>
                            <option value="Wendy's">Wendy's</option>
                            <option value="Starbucks">Starbucks</option>
                            <option value="Dunkin'">Dunkin' Donuts</option>
                            <option value="Chick-fil-A">Chick-fil-A</option>
                            <option value="Popeyes">Popeyes</option>
                            <option value="Arby's">Arby's</option>
                            <option value="White Castle">White Castle</option>
                            <option value="Sonic Drive-In">Sonic Drive-In</option>
                            <option value="Jack in the Box">Jack in the Box</option>
                            <option value="Carl's Jr">Carl's Jr.</option>
                            <option value="Hardee's">Hardee's</option>
                            <option value="Whataburger">Whataburger</option>
                            <option value="In-N-Out Burger">In-N-Out Burger</option>
                            <option value="Five Guys">Five Guys</option>
                            <option value="Shake Shack">Shake Shack</option>
                            <option value="Culver's">Culver's</option>
                            <option value="Steak 'n Shake">Steak 'n Shake</option>
                            <option value="Denny's">Denny's</option>
                            <option value="IHOP">IHOP</option>
                            <option value="Waffle House">Waffle House</option>
                            <option value="Cracker Barrel">Cracker Barrel</option>
                            <option value="Red Lobster">Red Lobster</option>
                            <option value="Olive Garden">Olive Garden</option>
                            <option value="Applebee's">Applebee's</option>
                            <option value="TGI Fridays">TGI Fridays</option>
                            <option value="Buffalo Wild Wings">Buffalo Wild Wings</option>
                            <option value="Outback Steakhouse">Outback Steakhouse</option>
                            <option value="Texas Roadhouse">Texas Roadhouse</option>
                            <option value="LongHorn Steakhouse">LongHorn Steakhouse</option>
                            <option value="The Cheesecake Factory">The Cheesecake Factory</option>
                            <option value="PF Chang's">P.F. Chang's</option>
                            <option value="Panda Express">Panda Express</option>
                            <option value="Chipotle">Chipotle</option>
                            <option value="Qdoba">Qdoba</option>
                            <option value="Moe's Southwest Grill">Moe's Southwest Grill</option>
                            <option value="Baja Fresh">Baja Fresh</option>
                            <option value="Del Taco">Del Taco</option>
                            <option value="El Pollo Loco">El Pollo Loco</option>
                            <option value="Blimpie">Blimpie</option>
                            <option value="Quiznos">Quiznos</option>
                            <option value="Jersey Mike's">Jersey Mike's</option>
                            <option value="Firehouse Subs">Firehouse Subs</option>
                            <option value="Jimmy John's">Jimmy John's</option>
                            <option value="Potbelly">Potbelly Sandwich Shop</option>
                            <option value="Corner Bakery">Corner Bakery Cafe</option>
                            <option value="Einstein Bros">Einstein Bros. Bagels</option>
                            <option value="Bruegger's">Bruegger's Bagels</option>
                            <option value="Krispy Kreme">Krispy Kreme</option>
                            <option value="Cinnabon">Cinnabon</option>
                            <option value="Auntie Anne's">Auntie Anne's</option>
                            <option value="Baskin-Robbins">Baskin-Robbins</option>
                            <option value="Cold Stone Creamery">Cold Stone Creamery</option>
                            <option value="Häagen-Dazs">Häagen-Dazs</option>
                            <option value="Ben & Jerry's">Ben & Jerry's</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="location">Location:</label>
                        <select id="location" name="location" required>
                            <option value="">Select a location...</option>
                            <option value="New York, NY">New York, NY</option>
                            <option value="Los Angeles, CA">Los Angeles, CA</option>
                            <option value="Chicago, IL">Chicago, IL</option>
                            <option value="Houston, TX">Houston, TX</option>
                            <option value="Phoenix, AZ">Phoenix, AZ</option>
                            <option value="Philadelphia, PA">Philadelphia, PA</option>
                            <option value="San Antonio, TX">San Antonio, TX</option>
                            <option value="San Diego, CA">San Diego, CA</option>
                            <option value="Dallas, TX">Dallas, TX</option>
                            <option value="San Jose, CA">San Jose, CA</option>
                            <option value="Austin, TX">Austin, TX</option>
                            <option value="Jacksonville, FL">Jacksonville, FL</option>
                            <option value="Fort Worth, TX">Fort Worth, TX</option>
                            <option value="Columbus, OH">Columbus, OH</option>
                            <option value="Charlotte, NC">Charlotte, NC</option>
                            <option value="San Francisco, CA">San Francisco, CA</option>
                            <option value="Indianapolis, IN">Indianapolis, IN</option>
                            <option value="Seattle, WA">Seattle, WA</option>
                            <option value="Denver, CO">Denver, CO</option>
                            <option value="Washington, DC">Washington, DC</option>
                            <option value="Boston, MA">Boston, MA</option>
                            <option value="El Paso, TX">El Paso, TX</option>
                            <option value="Nashville, TN">Nashville, TN</option>
                            <option value="Detroit, MI">Detroit, MI</option>
                            <option value="Oklahoma City, OK">Oklahoma City, OK</option>
                            <option value="Portland, OR">Portland, OR</option>
                            <option value="Las Vegas, NV">Las Vegas, NV</option>
                            <option value="Memphis, TN">Memphis, TN</option>
                            <option value="Louisville, KY">Louisville, KY</option>
                            <option value="Baltimore, MD">Baltimore, MD</option>
                            <option value="Milwaukee, WI">Milwaukee, WI</option>
                            <option value="Albuquerque, NM">Albuquerque, NM</option>
                            <option value="Tucson, AZ">Tucson, AZ</option>
                            <option value="Fresno, CA">Fresno, CA</option>
                            <option value="Sacramento, CA">Sacramento, CA</option>
                            <option value="Mesa, AZ">Mesa, AZ</option>
                            <option value="Kansas City, MO">Kansas City, MO</option>
                            <option value="Atlanta, GA">Atlanta, GA</option>
                            <option value="Long Beach, CA">Long Beach, CA</option>
                            <option value="Colorado Springs, CO">Colorado Springs, CO</option>
                            <option value="Raleigh, NC">Raleigh, NC</option>
                            <option value="Miami, FL">Miami, FL</option>
                            <option value="Virginia Beach, VA">Virginia Beach, VA</option>
                            <option value="Omaha, NE">Omaha, NE</option>
                            <option value="Oakland, CA">Oakland, CA</option>
                            <option value="Minneapolis, MN">Minneapolis, MN</option>
                            <option value="Tulsa, OK">Tulsa, OK</option>
                            <option value="Arlington, TX">Arlington, TX</option>
                            <option value="Tampa, FL">Tampa, FL</option>
                            <option value="New Orleans, LA">New Orleans, LA</option>
                            <option value="Wichita, KS">Wichita, KS</option>
                            <option value="Cleveland, OH">Cleveland, OH</option>
                            <option value="Bakersfield, CA">Bakersfield, CA</option>
                            <option value="Aurora, CO">Aurora, CO</option>
                            <option value="Anaheim, CA">Anaheim, CA</option>
                            <option value="Honolulu, HI">Honolulu, HI</option>
                            <option value="Santa Ana, CA">Santa Ana, CA</option>
                            <option value="Corpus Christi, TX">Corpus Christi, TX</option>
                            <option value="Riverside, CA">Riverside, CA</option>
                            <option value="Lexington, KY">Lexington, KY</option>
                            <option value="Stockton, CA">Stockton, CA</option>
                            <option value="Toledo, OH">Toledo, OH</option>
                            <option value="St. Paul, MN">St. Paul, MN</option>
                            <option value="Newark, NJ">Newark, NJ</option>
                            <option value="Greensboro, NC">Greensboro, NC</option>
                            <option value="Plano, TX">Plano, TX</option>
                            <option value="Henderson, NV">Henderson, NV</option>
                            <option value="Lincoln, NE">Lincoln, NE</option>
                            <option value="Buffalo, NY">Buffalo, NY</option>
                            <option value="Jersey City, NJ">Jersey City, NJ</option>
                            <option value="Chula Vista, CA">Chula Vista, CA</option>
                            <option value="Fort Wayne, IN">Fort Wayne, IN</option>
                            <option value="Orlando, FL">Orlando, FL</option>
                            <option value="St. Petersburg, FL">St. Petersburg, FL</option>
                            <option value="Chandler, AZ">Chandler, AZ</option>
                            <option value="Laredo, TX">Laredo, TX</option>
                            <option value="Norfolk, VA">Norfolk, VA</option>
                            <option value="Durham, NC">Durham, NC</option>
                            <option value="Madison, WI">Madison, WI</option>
                            <option value="Lubbock, TX">Lubbock, TX</option>
                            <option value="Irvine, CA">Irvine, CA</option>
                            <option value="Winston-Salem, NC">Winston-Salem, NC</option>
                            <option value="Glendale, AZ">Glendale, AZ</option>
                            <option value="Garland, TX">Garland, TX</option>
                            <option value="Hialeah, FL">Hialeah, FL</option>
                            <option value="Reno, NV">Reno, NV</option>
                            <option value="Chesapeake, VA">Chesapeake, VA</option>
                            <option value="Gilbert, AZ">Gilbert, AZ</option>
                            <option value="Baton Rouge, LA">Baton Rouge, LA</option>
                            <option value="Irving, TX">Irving, TX</option>
                            <option value="Scottsdale, AZ">Scottsdale, AZ</option>
                            <option value="North Las Vegas, NV">North Las Vegas, NV</option>
                            <option value="Fremont, CA">Fremont, CA</option>
                            <option value="Boise, ID">Boise, ID</option>
                            <option value="Richmond, VA">Richmond, VA</option>
                            <option value="San Bernardino, CA">San Bernardino, CA</option>
                            <option value="Birmingham, AL">Birmingham, AL</option>
                            <option value="Spokane, WA">Spokane, WA</option>
                            <option value="Rochester, NY">Rochester, NY</option>
                            <option value="Des Moines, IA">Des Moines, IA</option>
                            <option value="Modesto, CA">Modesto, CA</option>
                            <option value="Fayetteville, NC">Fayetteville, NC</option>
                            <option value="Tacoma, WA">Tacoma, WA</option>
                            <option value="Oxnard, CA">Oxnard, CA</option>
                            <option value="Fontana, CA">Fontana, CA</option>
                            <option value="Columbus, GA">Columbus, GA</option>
                            <option value="Montgomery, AL">Montgomery, AL</option>
                            <option value="Moreno Valley, CA">Moreno Valley, CA</option>
                            <option value="Shreveport, LA">Shreveport, LA</option>
                            <option value="Aurora, IL">Aurora, IL</option>
                            <option value="Yonkers, NY">Yonkers, NY</option>
                            <option value="Akron, OH">Akron, OH</option>
                            <option value="Huntington Beach, CA">Huntington Beach, CA</option>
                            <option value="Little Rock, AR">Little Rock, AR</option>
                            <option value="Augusta, GA">Augusta, GA</option>
                            <option value="Amarillo, TX">Amarillo, TX</option>
                            <option value="Glendale, CA">Glendale, CA</option>
                            <option value="Mobile, AL">Mobile, AL</option>
                            <option value="Grand Rapids, MI">Grand Rapids, MI</option>
                            <option value="Salt Lake City, UT">Salt Lake City, UT</option>
                            <option value="Tallahassee, FL">Tallahassee, FL</option>
                            <option value="Huntsville, AL">Huntsville, AL</option>
                            <option value="Grand Prairie, TX">Grand Prairie, TX</option>
                            <option value="Knoxville, TN">Knoxville, TN</option>
                            <option value="Worcester, MA">Worcester, MA</option>
                            <option value="Newport News, VA">Newport News, VA</option>
                            <option value="Brownsville, TX">Brownsville, TX</option>
                            <option value="Overland Park, KS">Overland Park, KS</option>
                            <option value="Santa Clarita, CA">Santa Clarita, CA</option>
                            <option value="Providence, RI">Providence, RI</option>
                            <option value="Garden Grove, CA">Garden Grove, CA</option>
                            <option value="Chattanooga, TN">Chattanooga, TN</option>
                            <option value="Oceanside, CA">Oceanside, CA</option>
                            <option value="Jackson, MS">Jackson, MS</option>
                            <option value="Fort Lauderdale, FL">Fort Lauderdale, FL</option>
                            <option value="Santa Rosa, CA">Santa Rosa, CA</option>
                            <option value="Rancho Cucamonga, CA">Rancho Cucamonga, CA</option>
                            <option value="Port St. Lucie, FL">Port St. Lucie, FL</option>
                            <option value="Tempe, AZ">Tempe, AZ</option>
                            <option value="Ontario, CA">Ontario, CA</option>
                            <option value="Vancouver, WA">Vancouver, WA</option>
                            <option value="Sioux Falls, SD">Sioux Falls, SD</option>
                            <option value="Springfield, MO">Springfield, MO</option>
                            <option value="Peoria, AZ">Peoria, AZ</option>
                            <option value="Pembroke Pines, FL">Pembroke Pines, FL</option>
                            <option value="Elk Grove, CA">Elk Grove, CA</option>
                            <option value="Salem, OR">Salem, OR</option>
                            <option value="Lancaster, CA">Lancaster, CA</option>
                            <option value="Corona, CA">Corona, CA</option>
                            <option value="Eugene, OR">Eugene, OR</option>
                            <option value="Palmdale, CA">Palmdale, CA</option>
                            <option value="Salinas, CA">Salinas, CA</option>
                            <option value="Springfield, MA">Springfield, MA</option>
                            <option value="Pasadena, TX">Pasadena, TX</option>
                            <option value="Fort Collins, CO">Fort Collins, CO</option>
                            <option value="Hayward, CA">Hayward, CA</option>
                            <option value="Pomona, CA">Pomona, CA</option>
                            <option value="Cary, NC">Cary, NC</option>
                            <option value="Rockford, IL">Rockford, IL</option>
                            <option value="Alexandria, VA">Alexandria, VA</option>
                            <option value="Escondido, CA">Escondido, CA</option>
                            <option value="McKinney, TX">McKinney, TX</option>
                            <option value="Kansas City, KS">Kansas City, KS</option>
                            <option value="Joliet, IL">Joliet, IL</option>
                            <option value="Sunnyvale, CA">Sunnyvale, CA</option>
                            <option value="Torrance, CA">Torrance, CA</option>
                            <option value="Bridgeport, CT">Bridgeport, CT</option>
                            <option value="Lakewood, CO">Lakewood, CO</option>
                            <option value="Hollywood, FL">Hollywood, FL</option>
                            <option value="Paterson, NJ">Paterson, NJ</option>
                            <option value="Naperville, IL">Naperville, IL</option>
                            <option value="Syracuse, NY">Syracuse, NY</option>
                            <option value="Mesquite, TX">Mesquite, TX</option>
                            <option value="Dayton, OH">Dayton, OH</option>
                            <option value="Savannah, GA">Savannah, GA</option>
                            <option value="Clarksville, TN">Clarksville, TN</option>
                            <option value="Orange, CA">Orange, CA</option>
                            <option value="Pasadena, CA">Pasadena, CA</option>
                            <option value="Fullerton, CA">Fullerton, CA</option>
                            <option value="Killeen, TX">Killeen, TX</option>
                            <option value="Frisco, TX">Frisco, TX</option>
                            <option value="Hampton, VA">Hampton, VA</option>
                            <option value="McAllen, TX">McAllen, TX</option>
                            <option value="Warren, MI">Warren, MI</option>
                            <option value="West Valley City, UT">West Valley City, UT</option>
                            <option value="Columbia, SC">Columbia, SC</option>
                            <option value="Olathe, KS">Olathe, KS</option>
                            <option value="Sterling Heights, MI">Sterling Heights, MI</option>
                            <option value="New Haven, CT">New Haven, CT</option>
                            <option value="Miramar, FL">Miramar, FL</option>
                            <option value="Waco, TX">Waco, TX</option>
                            <option value="Thousand Oaks, CA">Thousand Oaks, CA</option>
                            <option value="Cedar Rapids, IA">Cedar Rapids, IA</option>
                            <option value="Charleston, SC">Charleston, SC</option>
                            <option value="Visalia, CA">Visalia, CA</option>
                            <option value="Topeka, KS">Topeka, KS</option>
                            <option value="Elizabeth, NJ">Elizabeth, NJ</option>
                            <option value="Gainesville, FL">Gainesville, FL</option>
                            <option value="Thornton, CO">Thornton, CO</option>
                            <option value="Roseville, CA">Roseville, CA</option>
                            <option value="Carrollton, TX">Carrollton, TX</option>
                            <option value="Coral Springs, FL">Coral Springs, FL</option>
                            <option value="Stamford, CT">Stamford, CT</option>
                            <option value="Simi Valley, CA">Simi Valley, CA</option>
                            <option value="Concord, CA">Concord, CA</option>
                            <option value="Hartford, CT">Hartford, CT</option>
                            <option value="Kent, WA">Kent, WA</option>
                            <option value="Lafayette, LA">Lafayette, LA</option>
                            <option value="Midland, TX">Midland, TX</option>
                            <option value="Hayward, CA">Hayward, CA</option>
                            <option value="Billings, MT">Billings, MT</option>
                            <option value="West Palm Beach, FL">West Palm Beach, FL</option>
                            <option value="Columbia, MO">Columbia, MO</option>
                            <option value="Santa Clara, CA">Santa Clara, CA</option>
                            <option value="Portland, ME">Portland, ME</option>
                            <option value="South Bend, IN">South Bend, IN</option>
                            <option value="Downey, CA">Downey, CA</option>
                            <option value="Temecula, CA">Temecula, CA</option>
                            <option value="Norman, OK">Norman, OK</option>
                            <option value="Waterbury, CT">Waterbury, CT</option>
                            <option value="Santa Maria, CA">Santa Maria, CA</option>
                            <option value="Elgin, IL">Elgin, IL</option>
                            <option value="Murfreesboro, TN">Murfreesboro, TN</option>
                            <option value="Clearwater, FL">Clearwater, FL</option>
                            <option value="Wichita Falls, TX">Wichita Falls, TX</option>
                            <option value="Independence, MO">Independence, MO</option>
                            <option value="Provo, UT">Provo, UT</option>
                            <option value="West Jordan, UT">West Jordan, UT</option>
                            <option value="Fairfield, CA">Fairfield, CA</option>
                            <option value="Berkeley, CA">Berkeley, CA</option>
                            <option value="High Point, NC">High Point, NC</option>
                            <option value="Murrieta, CA">Murrieta, CA</option>
                            <option value="Antioch, CA">Antioch, CA</option>
                            <option value="Inglewood, CA">Inglewood, CA</option>
                            <option value="Richmond, CA">Richmond, CA</option>
                            <option value="West Covina, CA">West Covina, CA</option>
                            <option value="Gresham, OR">Gresham, OR</option>
                            <option value="Arvada, CO">Arvada, CO</option>
                            <option value="Boulder, CO">Boulder, CO</option>
                            <option value="Green Bay, WI">Green Bay, WI</option>
                            <option value="Daly City, CA">Daly City, CA</option>
                            <option value="Burbank, CA">Burbank, CA</option>
                            <option value="Rialto, CA">Rialto, CA</option>
                            <option value="Las Cruces, NM">Las Cruces, NM</option>
                            <option value="El Cajon, CA">El Cajon, CA</option>
                            <option value="San Mateo, CA">San Mateo, CA</option>
                            <option value="Compton, CA">Compton, CA</option>
                            <option value="Jurupa Valley, CA">Jurupa Valley, CA</option>
                            <option value="Vista, CA">Vista, CA</option>
                            <option value="South Gate, CA">South Gate, CA</option>
                            <option value="Mission Viejo, CA">Mission Viejo, CA</option>
                            <option value="Vacaville, CA">Vacaville, CA</option>
                            <option value="Carson, CA">Carson, CA</option>
                            <option value="Hesperia, CA">Hesperia, CA</option>
                            <option value="Santa Monica, CA">Santa Monica, CA</option>
                            <option value="Westminster, CA">Westminster, CA</option>
                            <option value="Redding, CA">Redding, CA</option>
                            <option value="Santa Barbara, CA">Santa Barbara, CA</option>
                            <option value="Chico, CA">Chico, CA</option>
                            <option value="Newport Beach, CA">Newport Beach, CA</option>
                            <option value="San Leandro, CA">San Leandro, CA</option>
                            <option value="Hawthorne, CA">Hawthorne, CA</option>
                            <option value="Citrus Heights, CA">Citrus Heights, CA</option>
                            <option value="Tracy, CA">Tracy, CA</option>
                            <option value="Alhambra, CA">Alhambra, CA</option>
                            <option value="Livermore, CA">Livermore, CA</option>
                            <option value="Buena Park, CA">Buena Park, CA</option>
                            <option value="Menifee, CA">Menifee, CA</option>
                            <option value="Hemet, CA">Hemet, CA</option>
                            <option value="Lakewood, CA">Lakewood, CA</option>
                            <option value="Merced, CA">Merced, CA</option>
                            <option value="Chino, CA">Chino, CA</option>
                            <option value="Redwood City, CA">Redwood City, CA</option>
                            <option value="Lake Forest, CA">Lake Forest, CA</option>
                            <option value="Napa, CA">Napa, CA</option>
                            <option value="Redlands, CA">Redlands, CA</option>
                            <option value="Turlock, CA">Turlock, CA</option>
                            <option value="Manteca, CA">Manteca, CA</option>
                            <option value="Whittier, CA">Whittier, CA</option>
                            <option value="Newport News, VA">Newport News, VA</option>
                            <option value="Costa Mesa, CA">Costa Mesa, CA</option>
                            <option value="Hawthorne, CA">Hawthorne, CA</option>
                            <option value="Citrus Heights, CA">Citrus Heights, CA</option>
                            <option value="Tracy, CA">Tracy, CA</option>
                            <option value="Alhambra, CA">Alhambra, CA</option>
                            <option value="Livermore, CA">Livermore, CA</option>
                            <option value="Buena Park, CA">Buena Park, CA</option>
                            <option value="Menifee, CA">Menifee, CA</option>
                            <option value="Hemet, CA">Hemet, CA</option>
                            <option value="Lakewood, CA">Lakewood, CA</option>
                            <option value="Merced, CA">Merced, CA</option>
                            <option value="Chino, CA">Chino, CA</option>
                            <option value="Redwood City, CA">Redwood City, CA</option>
                            <option value="Lake Forest, CA">Lake Forest, CA</option>
                            <option value="Napa, CA">Napa, CA</option>
                            <option value="Redlands, CA">Redlands, CA</option>
                            <option value="Turlock, CA">Turlock, CA</option>
                            <option value="Manteca, CA">Manteca, CA</option>
                            <option value="Whittier, CA">Whittier, CA</option>
                            <option value="Newport News, VA">Newport News, VA</option>
                            <option value="Costa Mesa, CA">Costa Mesa, CA</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit">Find Bad Reviews</button>
            </form>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            
            {% if results %}
            <div class="results">
                <div class="stats">
                    <h3>Analysis Results</h3>
                    <p><strong>Business:</strong> {{ business_name }}</p>
                    <p><strong>Location:</strong> {{ location }}</p>
                    <p><strong>Total Reviews Found:</strong> {{ total_reviews }}</p>
                    <p><strong>Bad Reviews:</strong> {{ bad_reviews_count }} ({{ bad_percentage }}%)</p>
                    <p><strong>Good Reviews:</strong> {{ good_reviews_count }} ({{ good_percentage }}%)</p>
                </div>
                
                {% if businesses %}
                <h3>Found Businesses:</h3>
                {% for business in businesses %}
                <div class="business">
                    <h3>{{ business.name }}</h3>
                    <div class="business-info">Address: {{ business.formatted_address }}</div>
                    <div class="business-info">Rating: <span class="rating">{{ business.rating }} stars</span></div>
                    <div class="business-info">Total Reviews: {{ business.user_ratings_total }}</div>
                </div>
                {% endfor %}
                {% endif %}
                
                {% if bad_reviews %}
                <h3>Bad Reviews ({{ bad_reviews|length }} found):</h3>
                {% for review in bad_reviews %}
                <div class="bad-review">
                    <div class="rating">{{ review.rating }} stars</div>
                    <div class="reviewer">Reviewer: {{ review.user.name }}</div>
                    <div class="review-text">{{ review.text }}</div>
                </div>
                {% endfor %}
                {% else %}
                <div class="success">
                    <h3>Great News!</h3>
                    <p>No bad reviews found! This business has good ratings.</p>
                </div>
                {% endif %}
                
                {% if all_reviews %}
                <div class="all-reviews">
                    <h3>All Reviews ({{ all_reviews|length }} total):</h3>
                    {% for review in all_reviews %}
                    <div class="review-item {% if review.rating < 4 %}bad{% else %}good{% endif %}">
                        <div class="review-rating {% if review.rating < 4 %}bad{% else %}good{% endif %}">
                            {{ review.rating }} stars
                        </div>
                        <div class="reviewer">Reviewer: {{ review.user.name }}</div>
                        <div class="review-text">{{ review.text }}</div>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        business_name = request.form.get('business_name', '').strip()
        location = request.form.get('location', '').strip()
        
        if not business_name or not location:
            return render_template_string(HTML_TEMPLATE, error="Please select both business name and location")
        
        try:
            # Search for businesses
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                return render_template_string(HTML_TEMPLATE, error="API key not found. Please check your .env file")
            
            businesses = search_businesses(business_name, location, api_key)
            
            if not businesses:
                return render_template_string(HTML_TEMPLATE, error=f"No businesses found for '{business_name}' in '{location}'")
            
            # Get reviews for the first business
            business = businesses[0]
            analyzer = GooglePlacesReviewAnalyzer()
            reviews = analyzer.get_business_reviews(business['place_id'])
            
            # Filter reviews
            bad_reviews = [review for review in reviews if review['rating'] < 4]
            good_reviews = [review for review in reviews if review['rating'] >= 4]
            
            total_reviews = len(reviews)
            bad_reviews_count = len(bad_reviews)
            good_reviews_count = len(good_reviews)
            bad_percentage = round((bad_reviews_count / total_reviews * 100), 1) if total_reviews > 0 else 0
            good_percentage = round((good_reviews_count / total_reviews * 100), 1) if total_reviews > 0 else 0
            
            return render_template_string(
                HTML_TEMPLATE,
                business_name=business_name,
                location=location,
                businesses=businesses,
                bad_reviews=bad_reviews,
                all_reviews=reviews,
                total_reviews=total_reviews,
                bad_reviews_count=bad_reviews_count,
                good_reviews_count=good_reviews_count,
                bad_percentage=bad_percentage,
                good_percentage=good_percentage
            )
            
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=f"Error: {str(e)}")
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting Enhanced Business Bad Review Finder...")
    print("Open your browser and go to: http://localhost:5000")
    print("This version shows ALL reviews, not just bad ones!")
    print("Press Ctrl+C to stop the server")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
