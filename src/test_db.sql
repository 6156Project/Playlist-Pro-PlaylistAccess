create database if not exists PlaylistAccess;
use PlaylistAccess;

drop table if exists PlaylistAccess.UserPlaylist;
drop table if exists PlaylistAccess.User;
drop table if exists PlaylistAccess.Playlist;


create table PlaylistAccess.UserPlaylist (
	userId varchar(36) not null,
  	playlistId varchar(36) not null,
  	ownerId varchar(36) not null,
  	primary key (userId, playlistId, ownerId)

);




insert into UserPlaylist(userId, playlistId, ownerId)
values ("uid-1", "pid-1", "uid-1"),
       ("uid-2", "pid-1", "uid-1"),
       ("uid-3", "pid-2", "uid-3"),
       ("uid-3", "pid-1", "uid-1");