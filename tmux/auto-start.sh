#!/usr/bin/env bash

session_name="work"

tmux new -d -s $session_name
tmux new-window -t $session_name:1 -n project
tmux new-window -t $session_name:2 -n local
tmux new-window -t $session_name:3 -n 30.250
tmux new-window -t $session_name:4 -n 30.111

tmux send -t $session_name:1 "j project" Enter
tmux send -t $session_name:2 "j pyzbs" Enter
tmux send -t $session_name:3 "ssh 192.168.30.250 & " Enter
tmux send -t $session_name:4 "pssh 30.111" Enter

tmux ls |grep $session_name
tmux attach -t $session_name
