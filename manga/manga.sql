create database if not exists mangareader;
use mangareader;

drop table if exists chapter;
drop table if exists picture;
drop table if exists project;
drop table if exists lacklist;

create table project(
	projectname varchar(100) primary key,
	homepage varchar(100),
	chapterdomain varchar(100),
   ifall bool default False
);

create table chapter(
	chaptername char(10),
	maxpicture tinyint(10),
	ifcomplete bool default False,
	projectname varchar(100),
	foreign key(projectname) references project(projectname)
);

create table picture(
	pictureurl varchar(100) primary key,
	projectname varchar(100),
	chaptername char(10),
	foreign key(projectname) references project(projectname)
);

create table lacklist(
	pictureurl varchar(100) primary key,
	chaptername char(10),
	projectname varchar(100)
);

	 select pictureurl from (
			select lacklist.pictureurl from lacklist, picture where lacklist.pictureurl = picture.pictureurl
	 ) as temp
);

select count(*) from lacklist;

select count(*), projectname from chapter where ifcomplete = 0 group by projectname;

select maxpicture, count(*) from chapter, picture
    where chapter.projectname = picture.projectname and chapter.chaptername = picture.chaptername;

insert into project(projectname, homepage) values('Ajin','http://www.goodmanga.net/6792/ajin');

insert into project (projectname, homepage, ifall)
values('One Piece','http://www.goodmanga.net/5/one_piece',0),('Platinum End','http://www.goodmanga.net/14017/platina-end',1);

select * from project;

select * from chapter where projectname like 'One%';

select picture.projectname, chapter.chaptername, maxpicture, count(*), ifcomplete from chapter,picture
where chapter.projectname = picture.projectname and chapter.chaptername = picture.chaptername
group by picture.projectname, picture.chaptername having maxpicture <> count(*);

select * from chapter where ifcomplete <> 1;

select chapterdomain from project where projectname like 'M%';

delete from picture
where pictureurl in (
    select a from(
    select picture.pictureurl as a,count(*) as b, maxpicture as c, chapter.chaptername as d, chapter.projectname as e
    from picture, chapter
    where picture.chaptername = chapter.chaptername and picture.projectname =  chapter.projectname
    group by picture.projectname, picture.chaptername having count(*) > maxpicture) as temp0) ;

update picture set pictureurl = replace(pictureurl, ' ', '')
where pictureurl like '% %';

delete from picture where pictureurl like '% %';
delete from chapter where projectname like 'O%' and chaptername = '850'
delete from chapter where projectname like 'A%' and chapternam in ('10' ,'15')

delete from picture where projectname

update picture name set pictureurl = replace(pictureurl, ' ', '');
update picture name set chaptername = replace(chaptername, ' ', '');

