# Chat Room API

## Description

A chat room API that features private and public chats with multiple participants 
<br>
<br>

## DATABASE DESIGN
<br>

### USER

| first_name | char(64) |
| --- | --- |
| last_name | char(64) |
| username | char(64) |
| birthdate | date |
| bio | char(1000) |
| avatar | img |
| join_date | date |
| role | char(255) |
<br>

### MESSAGE

| sender | fk user |
| --- | --- |
| datetime | datetime |
| body | char(1000) |
| adjuct_image | img (default=none) |
<br>

### FILES

| type_name | char(255) |
| --- | --- |
| file | file |
| max_size_kbytes | int (default=5120) |
| sender | fk user |
| datetime | datetime |
<br>

### TOPIC

| name | char(64) |
| --- | --- |
| description | char(255) |
<br>

### CHATROOM

| name | char(255) |
| --- | --- |
| description | char(1000) |
| creation_date | date |
| public | bool(default=true) |
| topics | fk topic |
| min_age_required | int (default=13) |
| participants | fk user |
| messages | fk message |
| files | fk file |
<br>

### CHAT

| participants | fk user (max 2) |
| --- | --- |
| messages | fk message |
<br>