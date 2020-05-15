-- 1. Za studenta koji ima ocenu 8 ili 9 izra�unati iz koliko ispita je dobio ocenu
--    8 i iz koliko ispita je dobio ocenu 9. Izdvojiti indeks studenta, broj ispita
--    iz kojih je student dobio ocenu 8 i broj ispita iz kojih je student dobio ocenu 9.
-- 1. nacin
with student_ocena as 
(
 select indeks, ocena ocena8, null ocena9
 from ispit
 where ocena = 8
 
 union all
 
 select indeks, null ocena8, ocena ocena9
 from ispit
 where ocena = 9
)
select indeks, count(ocena8) br8, count(ocena9) br9
from student_ocena
group by indeks;

-- 2. nacin
with stud8 as
(
 select indeks, count br8
 from ispit
 where ocena = 8
 group by indeks
),
stud9 as
(
 select indeks, count br9
 from ispit 
 where ocena = 9
 group by indeks
)
select coalesce(stud8.indeks, stud9.indeks) indeks,
	coalesce(br8, 0), coalesce(br9, 0)
from stud8 full join stud9
	on stud8.indeks = stud9.indeks;
	
-- 3. nacin (najefikasnije)
-- umesto count mozemo da koristimo i sum, vracamo vrednosti 0 ili 1
select indeks,
    count(case
		when ocena = 8 then ocena
		else null
	end) br8,
	count(case
		when ocena = 9 then ocena
		else null
	end) br9
from ispit
where ocena in (8, 9)
group by indeks;

-- 2. U tabelu dosije uneti novog studenta Marka Markovica sa indeksom 28/2012,
--    koji je ro�en 10.5.1990. godine u Kragujevcu.
insert into dosije (indeks, ime, prezime, datum_rodjenja, mesto_rodjenja, datum_upisa)
values(20120028, 'Marko', 'Markovic', '10.5.1990', 'Kragujevac', '03.07.2012');

-- 3. Uneti u bazu MSTUD podatke o predmetima: 
-- Uvod u arhitekturu ra�unara, koji ima �ifru P112, 6 bodova i identifikator 2005; 
-- Razvoj softvera, koji ima �ifru P116, 6 bodova i identifikator 2006.
insert into predmet (naziv, sifra, bodovi, id_predmeta)
values('Uvod u arhitekturu racunara', 'P112', 6, 2005),
	  ('Razvoj softvera', 'P116', 6, 2006);
	  
-- 4. Uneti podatke o polaganju ispita iz predmeta Programiranje 2 za studente ro�ene
--    1994. godine. Studenti su polagali u junskom ispitnom roku 2015. godine i svi 
--    su dobili ocenu 9. 
insert into ispit (indeks, id_predmeta, godina_roka, oznaka_roka, ocena)
select indeks, id_predmeta, 2015, 'jun', 9
from dosije, predmet
where year(datum_rodjenja) = 1994 
	and naziv = 'Programiranje 2';
	
-- 5. Iz baze izbrisati podatke o studentima ro�enim 1990. godine. 
delete from dosije
where year(datum_rodjenja) = 1990;

-- 6. Iz baze izbrisati ispite u kojima je polagan predmet Programiranje 2
--    ili predmet koji ima 15 bodova. 
delete from ispit
where id_predmeta in (select id_predmeta
					  from predmet
					  where bodovi = 15
					  	or naziv = 'Programiranje 2');

-- 7. Svim predmetima �ija �ifra po�inje sa P pove�ati broj bodova za 20%. 
update predmet
set bodovi = bodovi * 1.2
where naziv like 'P%';

-- 8. Svim studentima koji su u januaru 2015. godine polagali Analizu 1 promeniti
--    rok u jun 2015. Datum polaganja staviti da je nepoznat.
update ispit
set (oznaka_roka, datum_ispita) = ('jun', null)
where oznaka_roka = 'jan' 
	and godina_roka = 2015
	and id_predmeta in (select id_predmeta
						from predmet
						where naziv = 'Analiza 1');
						
-- 9. Predmetima koje su polagali studenti iz Beograda postaviti broj bodova na 
--    najve�i broj bodova koji postoji u tabeli predmet.
update predmet
set bodovi = (select max(bodovi)
			  from predmet)
where id_predmeta in (select id_predmeta
					  from ispit 
					  where indeks in (select indeks
					  				   from dosije
					  				   where mesto_rodjenja = 'Beograd'));
					  				   
-- 10. Prona�i studenta koji ima najvi�e polo�enih bodova. Izdvojiti indeks, 
--     ime i prezime studenta i broj polo�enih bodova.
select d.indeks, ime, prezime, sum(p.bodovi) espb
from dosije d join ispit i
		on d.indeks = i.indeks
	join predmet p
		on p.id_predmeta = i.id_predmeta
where ocena > 5
group by d.indeks, ime, prezime
having sum(p.bodovi) >= all (select sum(p1.bodovi)
							 from ispit i1 join predmet p1
							 	on i1.id_predmeta = p1.id_predmeta
							 where ocena > 5
							 group by indeks);
							 
-- ili 

with student as 
(
 select d.indeks, ime, prezime, sum(p.bodovi) espb
 from ispit i join dosije d
 		on d.indeks = i.indeks
 	join predmet p
 		on p.id_predmeta = i.id_predmeta
 where ocena > 5
 group by d.indeks, ime, prezime
)
select *
from student
where espb = (select max(espb)
			  from student);

-- 11. Za svakog studenta koji je polo�io izme�u 15 i 25 bodova i �ije ime 
--     sadr�i malo ili veliko slovo o ili a izdvojiti indeks, ime, prezime, 
--     broj predmeta koje je polagao, broj predmeta koje je polo�io i
--     prose�nu ocenu. Rezultat urediti prema indeksu.
select d.indeks, ime, prezime, 
	   count(distinct i.id_predmeta) "Polagani predmeti",
	   sum(case
	   		when ocena > 5 then 1
	   		else 0
	   	   end) "Polozeni predmeti", 
	   dec(avg(case
	   			when ocena > 5 then ocena*1.0
	   			else null
	   		   end), 4, 2) "Prosek"
from dosije d left join ispit i
		on d.indeks = i.indeks
	join predmet p
		on p.id_predmeta = i.id_predmeta
where lower(ime) like '%o%' or lower(ime) like '%a%'
group by d.indeks, ime, prezime
having sum(case
			when ocena > 5 then p.bodovi
			else 0
		   end) between 15 and 25
order by d.indeks;