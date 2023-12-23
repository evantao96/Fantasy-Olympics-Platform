select cNames,sumNames from (select c.name as cNames,count(a.id) as sumNames from Athletes a, Country c where a.country_id = c.id group by a.country_id) as sumTable order by sumNames;

USA - hot
Soviet Union - cold
Great Britain - wet
France - hot
Germany - hot
Italy - dry
Sweden - cold
Australia - dry
Hungary - cold
Netherlands - cold
Japan - hot
Canada - cold
China - hot
Russia - cold
Norway - cold
Denmark - cold
Romania - dry
Poland - hot
South Korea - wet
Spain - wet
