--Task 1
pers_anls = load '/home/nick/BDM_a1/personality_analysis.csv'  USING org.apache.pig.piggybank.storage.CSVExcelStorage(';', 'NO_MULTILINE', 'UNIX', 'SKIP_INPUT_HEADER') 
AS (ID:int ,Year_Birth:int ,Education:chararray 
,Marital_Status:chararray ,Income:int ,Kidhome:int ,Teenhome:int ,Dt_Customer:chararray ,Recency:int ,MntWines:int ,MntFruits:int ,MntMeatProducts:int ,MntFishProducts:int 
,MntSweetProducts:int ,MntGoldProds:int ,NumDealsPurchases:int ,NumWebPurchases:int ,NumCatalogPurchases:int ,NumStorePurchases:int ,NumWebVisitsMonth:int ,AcceptedCmp3: int 
,AcceptedCmp4: int ,AcceptedCmp5: int ,AcceptedCmp1: int ,AcceptedCmp2: int ,Complain: int ,Response: int );

-- fix null values on Income
SPLIT pers_anls INTO pers_anls_p1 IF Income is not null , pers_anls_p2 IF Income is null;
gr_pers_anls1_all = GROUP pers_anls_p1 all;

--calculate avg of income for all the non null rows
mean = FOREACH gr_pers_anls1_all {
		avg= AVG(pers_anls_p1.Income);
        generate flatten(pers_anls_p1),avg AS avg1;
};

--union the two parts with new column with values 0 and the average
pers_anls_p2 = FOREACH pers_anls_p2 GENERATE ID , Year_Birth , Education , Marital_Status , Income , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response, 0.0 AS tt:double;
pers_anls_p1 = FOREACH mean GENERATE ID , Year_Birth , Education , Marital_Status , Income, Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response, avg1 AS tt;
pers_anls = UNION ONSCHEMA pers_anls_p1, pers_anls_p2 ;

gr_pers_anls_all = GROUP pers_anls all;

--create a new column with the average Income. Actually it has the maximum value between 0 and the average Income
mean = FOREACH gr_pers_anls_all {
		max_value= MAX(pers_anls.tt);
		count = COUNT(pers_anls);
        generate flatten(pers_anls),max_value AS avg1, count AS count1;
};
--split the table again to "modify" the income where it is missing, and union again
SPLIT mean INTO pers_anls_p1 IF Income is not null , pers_anls_p2 IF Income is null;
pers_anls_p2 = FOREACH pers_anls_p2 GENERATE ID , Year_Birth , Education , Marital_Status , avg1 AS Income:int , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response, count1, avg1;
pers_anls_p1 = FOREACH pers_anls_p1 GENERATE ID , Year_Birth , Education , Marital_Status , Income , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response, count1, avg1;
pers_anls = UNION ONSCHEMA pers_anls_p1, pers_anls_p2 ;

-- now we are trying to calculate the standard deviation
mean = FOREACH pers_anls GENERATE *, (Income-avg1)*(Income-avg1) AS snd;
mean_all = GROUP mean all;
mean = FOREACH mean_all {
		snd_d= SUM(mean.snd);
        generate flatten(mean), snd_d  AS dev;
};
mean = FOREACH mean GENERATE *,  (SQRT(dev / count1)*3)+ avg1 AS outlier;

SPLIT mean INTO pers_anls_p1 IF Income<=outlier , pers_anls_p2 IF Income>outlier;
--split the table to "modify" the income where it it is bigger than our outlier , and union again
pers_anls_p2 = FOREACH pers_anls_p2 GENERATE ID , Year_Birth , Education , Marital_Status , avg1 AS Income:int , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response;
pers_anls_p1 = FOREACH pers_anls_p1 GENERATE ID , Year_Birth , Education , Marital_Status , Income , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response;
pers_anls = UNION ONSCHEMA pers_anls_p1, pers_anls_p2 ;




--we assume that there can't be a date birth before 1930
SPLIT pers_anls INTO pers_anls_p1 IF Year_Birth >1930 , pers_anls_p2 IF Year_Birth <= 1930;
gr_pers_anls1_all = GROUP pers_anls_p1 all;
--calculate avg of birth year for all valid values
pers_avg_bd = FOREACH gr_pers_anls1_all {
		avg= AVG(pers_anls_p1.Year_Birth);
        generate flatten(pers_anls_p1),avg AS avg_bd;
};
--union the two parts with new column with values 0 and the average birth year
pers_anls_p2 = FOREACH pers_anls_p2 GENERATE ID , Year_Birth , Education , Marital_Status , Income , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response, 0 AS tt:int;
pers_anls_p1 = FOREACH pers_avg_bd GENERATE ID , Year_Birth , Education , Marital_Status , Income, Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response, avg_bd AS tt:int;
pers_anls = UNION ONSCHEMA pers_anls_p1, pers_anls_p2 ;
--create a new column with the average birth year. Actually it has the maximum value between 0 and the average birth year
gr_pers_anls_all = GROUP pers_anls all;
pers_avg_bd = FOREACH gr_pers_anls_all {
		max_value= MAX(pers_anls.tt);
        generate flatten(pers_anls),max_value AS mean_bd;
};

--split the table again to "modify" the birth year where the values are not accepted by our assumptions
SPLIT pers_avg_bd INTO pers_anls_p1 IF Year_Birth >1930 , pers_anls_p2 IF Year_Birth <= 1930;
pers_anls_p2 = FOREACH pers_anls_p2 GENERATE ID , mean_bd AS Year_Birth , Education , Marital_Status , Income , Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response;
pers_anls_p1 = FOREACH pers_anls_p1 GENERATE ID , Year_Birth , Education , Marital_Status , Income, Kidhome , Teenhome , Dt_Customer , Recency , MntWines , MntFruits , MntMeatProducts , MntFishProducts , MntSweetProducts , MntGoldProds , NumDealsPurchases , NumWebPurchases , NumCatalogPurchases , NumStorePurchases , NumWebVisitsMonth , AcceptedCmp3 , AcceptedCmp4 , AcceptedCmp5 , AcceptedCmp1 , AcceptedCmp2 , Complain , Response;
pers_anls = UNION ONSCHEMA pers_anls_p1, pers_anls_p2 ;

--Store our changes new csv
STORE pers_anls INTO '/home/nick/BDM_a1/PostProccess' USING PigStorage(';');
fs -getmerge  /home/nick/BDM_a1/PostProccess /home/nick/BDM_a1/PostProccess.csv;

--Task 2
pers_anls = load '/home/nick/BDM_a1/PostProccess.csv'  using PigStorage(';') AS (ID:int ,Year_Birth:int ,Education:chararray 
,Marital_Status:chararray ,Income:int ,Kidhome:int ,Teenhome:int ,Dt_Customer:Datetime ,Recency:int ,MntWines:int ,MntFruits:int ,MntMeatProducts:int ,MntFishProducts:int 
,MntSweetProducts:int ,MntGoldProds:int ,NumDealsPurchases:int ,NumWebPurchases:int ,NumCatalogPurchases:int ,NumStorePurchases:int ,NumWebVisitsMonth:int ,AcceptedCmp3: int 
,AcceptedCmp4: int ,AcceptedCmp5: int ,AcceptedCmp1: int ,AcceptedCmp2: int ,Complain: int ,Response: int );

gr_pers_anls = Group pers_anls by Education;

pers_anls_Educc = foreach gr_pers_anls  Generate (pers_anls.Education), count(pers_anls); 
pers_anls_Educc = foreach gr_pers_anls  Generate flatten(group) as (Education), count(pers_anls.Education);
pers_anls_Educc = foreach gr_pers_anls  Generate (group), COUNT(pers_anls.Education);
kk= ORDER pers_anls_Educc by group;

STORE kk INTO '/home/nick/BDM_a1/Question2' USING PigStorage(';');
fs -getmerge  /home/nick/BDM_a1/Question2 /home/nick/BDM_a1/Question2.csv;

--Task 3

pers_anls = load '/home/nick/BDM_a1/PostProccess.csv'  using PigStorage(';') AS (ID:int ,Year_Birth:int ,Education:chararray 
,Marital_Status:chararray ,Income:int ,Kidhome:int ,Teenhome:int ,Dt_Customer:Datetime ,Recency:int ,MntWines:int ,MntFruits:int ,MntMeatProducts:int ,MntFishProducts:int 
,MntSweetProducts:int ,MntGoldProds:int ,NumDealsPurchases:int ,NumWebPurchases:int ,NumCatalogPurchases:int ,NumStorePurchases:int ,NumWebVisitsMonth:int ,AcceptedCmp3: int 
,AcceptedCmp4: int ,AcceptedCmp5: int ,AcceptedCmp1: int ,AcceptedCmp2: int ,Complain: int ,Response: int );

pers_anls = FOREACH pers_anls GENERATE *, 2022-Year_Birth AS age;
pers_anls = FOREACH pers_anls GENERATE ID, age, Education, Marital_Status, Income, MntWines ;

gr_pers_anls_all = Group pers_anls all;

mean_wine = foreach gr_pers_anls_all {
        sum = SUM(pers_anls.MntWines);
        count = COUNT(pers_anls);
        generate flatten(pers_anls), (3*sum)/(2*count) as bb, count as count, sum as ss;
};

B = FILTER mean_wine BY MntWines > bb;
ll= ORDER B by MntWines DESC, Income DESC;
ll = FOREACH ll GENERATE ID, age, Education, Marital_Status, Income, MntWines ;
c = rank ll;

STORE c INTO '/home/nick/BDM_a1/Question3' USING PigStorage(';');
fs -getmerge  /home/nick/BDM_a1/Question3 /home/nick/BDM_a1/Question3.csv;

--Task 4
pers_anls = load '/home/nick/BDM_a1/PostProccess.csv'  using PigStorage(';') AS (ID:int ,Year_Birth:int ,Education:chararray 
,Marital_Status:chararray ,Income:int ,Kidhome:int ,Teenhome:int ,Dt_Customer:chararray ,Recency:int ,MntWines:int ,MntFruits:int ,MntMeatProducts:int ,MntFishProducts:int 
,MntSweetProducts:int ,MntGoldProds:int ,NumDealsPurchases:int ,NumWebPurchases:int ,NumCatalogPurchases:int ,NumStorePurchases:int ,NumWebVisitsMonth:int ,AcceptedCmp3: int 
,AcceptedCmp4: int ,AcceptedCmp5: int ,AcceptedCmp1: int ,AcceptedCmp2: int ,Complain: int ,Response: int );

pers_anls = FOREACH pers_anls {
ind_of_y = (int) LAST_INDEX_OF(Dt_Customer,'/')+1;
size_of_y= ind_of_y+2;
total_spend=MntWines + MntFruits + MntMeatProducts + MntFishProducts + MntSweetProducts + MntGoldProds;

GENERATE *, SUBSTRING (Dt_Customer,ind_of_y,size_of_y) AS year, total_spend AS Mnt_Total;};

gr_pers_anls_all = Group pers_anls all;

mean_exp = foreach gr_pers_anls_all {
        sum = SUM(pers_anls.Mnt_Total);
        count = COUNT(pers_anls);
        generate flatten(pers_anls), (3*sum)/(2*count) as Mnt_thresh;
};
Filt_pers_anls = FILTER mean_exp BY Income > 69500 AND Mnt_Total>Mnt_thresh;


SPLIT Filt_pers_anls INTO gold IF year=='21', silver IF year!='21';
gold = FOREACH gold GENERATE 'Gold' as Cat, ID;
silver = FOREACH silver GENERATE 'Silver' as Cat, ID;

gold = ORDER gold BY ID DESC;
silver = ORDER silver BY ID DESC;

Res = UNION gold, silver;
f_res = Group Res by Cat;

f_res = FOREACH f_res GENERATE (group) AS rank, FLATTEN(TOTUPLE (Res.ID)) as nid;

STORE f_res INTO '/home/nick/BDM_a1/Question4' USING PigStorage(',');
fs -getmerge  /home/nick/BDM_a1/Question4 /home/nick/BDM_a1/Question4.csv;
