-- 1. Izdvojiti ukupan broj studenata.
select count(*) "Broj studenata"
from dosije;

-- 2. Izdvojiti ukupan broj studenata koji bar iz jednog predmeta imaju ocenu 10. 
select count "Broj studenata"
from dosije d
where exists (select *
			  from ispit i
			  where i.indeks = d.indeks
			  	and ocena = 10);
			  	
-- ili

select count(distinct indeks) "Broj studenata"
from ispit
where ocena = 10;

-- 3. Izdvojiti ukupan broj polo�enih predmeta i polo�enih bodova za studenta 
--    sa indeksom 25/2014.
select count "Broj polozenih predmeta", sum(p.bodovi) "Polozeni bodovi"
from ispit i join predmet p
	on i.id_predmeta = p.id_predmeta
where indeks = 20140025 and ocena > 5; 

-- 4. Izlistati ocene dobijene na ispitima i ako je ocena jednaka 5 ispisati NULL . 
select nullif(ocena, 5) "Ocene"
from ispit;

-- 5. Koliko ima razli�itih ocena dobijenih na ispitima, a da ocena nije 5?
select count(distinct ocena) "Broj razlicitih ocena"
from ispit
where ocena <> 5;

-- ili 
select count(distinct nullif(ocena, 5)) "Broj razlicitih ocena"
from ispit;

-- 6. Izdvojiti �ifre, nazive i bodove predmeta �iji je broj bodova ve�i od prose�nog
--     broja bodova svih predmeta.
select p.sifra, p.naziv, p.bodovi
from predmet p
where p.bodovi > all (select avg(bodovi)
					  from predmet
					  where id_predmeta <> p.id_predmeta);
					  
-- ili 
select p.sifra, p.naziv, p.bodovi
from predmet p
where p.bodovi > (select avg(bodovi)
				  from predmet);
				  
-- 7. Za svaki predmet izra�unati koliko studenata ga je polo�ilo. 
select count "Broj studenata po predmetu"
from ispit
where ocena > 5
group by id_predmeta;

-- 8. Za svakog studenta ro�enog 1995. godine, koji ima bar jedan polo�en ispit, 
--    izdvojiti broj indeksa, prose�nu ocenu, najmanju ocenu i najve�u ocenu iz 
--    polo�enih ispita. 
select i.indeks, dec(avg(ocena*1.0), 4, 2) "Prosek", 
	   min(ocena) "Najmanja ocena", max(ocena) "Najveca ocena"
from dosije d join ispit i
	on d.indeks = i.indeks
where year(datum_rodjenja) = 1995 and ocena > 5
group by i.indeks;

-- 9. Za svaku godinu ispitnog roka i predmet polagan u toj godini, prona�i najve�u
--    ocenu dobijenu na ispitima tog predmeta u toj godini. Izdvojiti godinu roka, 
--    naziv predmeta i najve�u ocenu. 
select godina_roka, p.naziv, max(ocena) "Najveca ocena"
from ispit i join predmet p
	on i.id_predmeta = p.id_predmeta
group by godina_roka, p.id_predmeta, p.naziv;

-- 10. Izdvojiti nazive predmeta koje je polagalo vi�e od 5 razli�itih studenata. 
select naziv
from predmet p join ispit i
	on p.id_predmeta = i.id_predmeta
group by naziv
having count(distinct indeks) > 5;

-- 11. Za svaki rok koji je odr�an u 2015. godini i u kome su svi polagani ispiti i
--     polo�eni, tj. nema ispita koji nije polo�en, izdvojiti oznaku roka, broj polo�enih 
--     ispita u tom roku i broj studenata koji su polo�ili ispite u tom roku.
select oznaka_roka, count "Broj polozenih ispita", count(distinct indeks) "Broj studenata"
from ispit
where godina_roka = 2015
group by oznaka_roka
having min(ocena) > 5;

-- 12. Za svaki predmet izdvojiti broj studenata koji su ga polagali. Izdvojiti naziv 
--     predmeta i broj studenata. Rezultat urediti prema broju studenata koji su polagali
--     predmet u opadaju�em poretku.
select naziv, count(distinct indeks) "Broj studenata"
from predmet p left join ispit i
	on i.id_predmeta = p.id_predmeta
group by naziv, p.id_predmeta
order by count(distinct indeks) desc;

-- 13. Za svakog studenta izdvojiti broj indeksa i mesec u kome je polo�io vi�e od dva ispita
--    (nije va�no koje godine). Izdvojiti indeks studenta, ime meseca i broj polo�enih predmeta.
--    Rezultat urediti prema broju indeksa i mesecu polaganja.
select indeks, monthname(datum_ispita) "Mesec", count(distinct id_predmeta) "Broj polozenih ispita"
from ispit
where ocena > 5
group by indeks, monthname(datum_ispita)
having count > 2
order by indeks, monthname(datum_ispita);

-- 14. Koliko ima studenata koji su polo�ili vi�e od 10 bodova?
select count "Broj studenata"
from (
		select indeks, sum(p.bodovi)
		from ispit i join predmet p
			on i.id_predmeta = p.id_predmeta
			and ocena > 5
		group by indeks
		having sum(p.bodovi) > 10) as t;
		
-- ili 

with student_bodovi as
(select indeks, sum(p.bodovi) "Polozeno" -- svaka kolona mora da ima ime
 from ispit i join predmet p
 	on i.id_predmeta = p.id_predmeta
 	and ocena > 5
 group by indeks
 having sum(p.bodovi) > 10)
 select count "Broj studenata"
 from student_bodovi;