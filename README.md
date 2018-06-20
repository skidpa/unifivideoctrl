# UniFiVideoCtrl
this project is still in it's early stages and currently not really usable since it requires cli interaction also the client is not yet available.

## What is this?
The idea is to have a server that can handle request's from clients to arm/disarm unifi surveillance cameras.

## Status
The following is the task list I'm currently working towards although things are being added continuously

- [ ] Api calls to UniFi-Video nvr
  - [x] Enable motion recording
  - [x] Disable motion recording
  - [ ] Enable continuous recording
  - [ ] Disable continuous recording
  - [x] Get camera list
  - [x] Log in/Log out
- [ ] Database
  - [x] Add cameras to the local database
  - [x] Load cameras from the local database
  - [x] Get password for authentication of client's
  - [ ] Encrypted database
  - [ ] Database credentials encrypted
  - [ ] Add camera zones to the database
- [ ] Server
  - [x] server running and can receive commands from client
  - [ ] Encrypted traffic

- [ ] Client
  - [ ] GUI
  - [x] Can connect to server.
  - [x] Can send traffic to server and get response back
  - [ ] Encrypted traffic
