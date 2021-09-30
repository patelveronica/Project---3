--Create brewery_beer table
Create table brewery_beer(
    beer_beerid bigint PRIMARY KEY,
    brewery_id bigint
)
-- Create Brewery table
CREATE TABLE brewery (
	brewery_id bigint PRIMARY KEY,
	brewery_name VARCHAR
	);
--Create Beer table
Create table beer(
	beer_beerid bigint primary key,
	brewery_id bigint,
	beer_name varchar,
	beer_style varchar,
	beer_abv double precision   
	)
--Create Reviews Table
Create table reviews(
	beer_id bigint,
	brewery_id bigint,
	review_overall double precision,
	review_aroma double precision,
	review_appearance double precision,
	review_palate double precision,
	review_taste double precision
)

----- Above tables are created with clean datasets -------
-------- find top 5 beer_id based on Max overall_review ------
select beer.beer_beerid, beer.beer_name,reviews.review_overall from beer
join reviews on beer.beer_beerid = reviews.beer_id
order by reviews.review_overall desc limit 5;

-- -- -- find top 10 beer_id based on Max review_aroma - you can find other features same way
select beer_name, review_aroma from reviews 
join beer on beer.beer_beerid = reviews.beer_beerid order by review_aroma desc limit 10;

