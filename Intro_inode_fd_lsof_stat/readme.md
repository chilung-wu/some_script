# inode, fd, fdinfo, file_table概念、`lsof`, `stat`用法

## 定義與關係

### `inode`（索引節點）

`inode` 是文件系統中存儲文件元數據的數據結構。每個文件或目錄都有一個唯一的 `inode`，包含了文件的所有元數據（例如文件大小、所有者、許可權、時間戳等），但不包含文件名或實際數據內容。

### `inode table`（索引節點表）

`inode table` 是一個數組，包含了文件系統中所有 `inode` 的列表。這個表在文件系統創建時初始化，並且每個 `inode` 在表中都有一個唯一的索引號（`inode number`）。

### `file descriptor`（文件描述符）

`file descriptor` 是一個非負整數，用於標識已打開文件的抽象指標。在程序打開文件時，操作系統會分配一個文件描述符給這個打開的文件，程序通過這個描述符進行讀寫操作。

### `file table`（文件表）

`file table` 是操作系統維護的一個全局結構，用於存儲有關所有打開文件的信息。每個文件表條目包含了文件的狀態、文件偏移量、文件描述符和對應的 `inode` 等信息。


### `關係圖` 

![alt text](image.png)
ref: [lusp_fileio_slides.pdf](https://man7.org/training/download/lusp_fileio_slides.pdf)


### 概念關係

1. **`inode` 與文件**：每個文件或目錄都有一個唯一的 `inode`，存儲了該文件或目錄的元數據。
2. **`inode table`**：包含了文件系統中所有 `inode` 的集合，是文件系統的核心結構之一。
3. **`file descriptor`**：當程序打開一個文件時，操作系統分配一個文件描述符。文件描述符指向文件表中的一個條目。
4. **`file table`**：文件表條目包含文件描述符、文件狀態、偏移量和指向 `inode` 的指針等信息。

## 操作步驟

### 創建示例文件和 C 程序

1. 創建一個文本文件 `example.txt`：

    ```bash
    echo "這是一個測試文件。" > example.txt
    ```

2. 創建一個 C 源碼文件 `open_example.c`，並將以下代碼複製進去：

    ```c
    #include <stdio.h>
    #include <fcntl.h>
    #include <unistd.h>

    int main() {
        int fd = open("example.txt", O_RDONLY);
        if (fd == -1) {
            perror("open");
            return 1;
        }
        printf("文件描述符: %d\n", fd);
        close(fd);
        return 0;
    }
    ```

### 編譯和運行程序

1. 使用 GCC 編譯程序：

    ```bash
    gcc -g -o open_example open_example.c
    ```

2. 或者，創建一個 `Makefile` 來編譯程序：

    ```Makefile
    all: open_example

    open_example: open_example.c
        gcc -g -o open_example open_example.c

    clean:
        rm -f open_example
    ```

    使用 `make` 命令編譯程序：

    ```bash
    make
    ```

1. **查看 `inode` 號**：

    ```bash
    ls -i example.txt
    ```

    輸出：

    ```plaintext
    2228242 example.txt
    ```

2. **查看文件詳細信息**：

    ```bash
    stat example.txt
    ```

    輸出：

    ```plaintext
        File: example.txt
        Size: 28              Blocks: 8          IO Block: 4096   regular file
    Device: 803h/2051d      Inode: 2228242     Links: 2
    Access: (0664/-rw-rw-r--)  Uid: ( 1000/ chilung)   Gid: ( 1000/ chilung)
    Access: 2024-05-15 18:29:03.239095269 +0800
    Modify: 2024-05-15 18:28:25.058493110 +0800
    Change: 2024-05-15 18:28:34.022940221 +0800
    Birth: 2024-05-15 18:28:25.058493110 +0800
    ```
    信息包括：

    - **File**：文件名
    - **Size**：文件大小（以字節為單位）
    - **Blocks**：文件使用的磁盤塊數量
    - **IO Block**：IO 區塊大小
    - **Device**：設備號
    - **Inode**：`inode` 號
    - **Links**：硬鏈接數量
    - **Access**：文件許可權和所有者（用八進制表示，如 `0664`，及文本表示如 `-rw-rw-r--`）
    - **Uid** 和 **Gid**：文件的用戶 ID 和組 ID，以及對應的用戶名和組名
    - **Access**：最近一次訪問時間
    - **Modify**：最近一次修改時間
    - **Change**：最近一次狀態更改時間
    - **Birth**：文件創建時間（如果文件系統支持）


### 使用 GDB 調試程序

1. 啟動 GDB 並設置斷點在 `printf` 前：

    ```bash
    gdb ./open_example
    ```

    在 GDB 中設置斷點並運行程序：

    ```gdb
    (gdb) break printf
    Breakpoint 1 at 0x4005e6: file open_example.c, line 8.
    (gdb) run
    Starting program: /tmp/open_example

    Breakpoint 1, main () at open_example.c:8
    8           printf("文件描述符: %d\n", fd);
    ```


2. ~~查找 GDB 中進程的 PID：~~

    ```gdb
    (gdb) !echo $$
    ```

### 使用 `lsof` 檢查文件描述符

1. 在另一個終端中使用 `lsof` 命令查看打開的文件：

    ```bash
    lsof -c open_example
    ```

    輸出：
    ```plaintext
    COMMAND    PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
    open_exam 6969 chilung  cwd    DIR    8,3    69632 2228225 /tmp
    open_exam 6969 chilung  rtd    DIR    8,3     4096       2 /
    open_exam 6969 chilung  txt    REG    8,3    17464 2228355 /tmp/open_example
    open_exam 6969 chilung  mem    REG    8,3  2220400 3672268 /usr/lib/x86_64-linux-gnu/libc.so.6
    open_exam 6969 chilung  mem    REG    8,3   240936 3672171 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    open_exam 6969 chilung    0u   CHR  136,3      0t0       6 /dev/pts/3
    open_exam 6969 chilung    1u   CHR  136,3      0t0       6 /dev/pts/3
    open_exam 6969 chilung    2u   CHR  136,3      0t0       6 /dev/pts/3
    open_exam 6969 chilung    3r   REG    8,3       28 2228242 /tmp/example.txt
    ```


### 檢查 `/proc/<PID>/fdinfo/<FD>`

1. 查看 `/proc/<PID>/fdinfo/<FD>` 以獲取文件描述符的詳細信息，例如：

    ```bash
    cat /proc/<PID>/fdinfo/3
    ```

    這將顯示類似以下的輸出：

    ```plaintext
    pos:    0
    flags:  0100000
    mnt_id: 29
    ino:    2228242
    ```

### 詳細解釋 `flags` 文件狀態標誌的含義

- **pos**：文件偏移量，表示當前文件讀寫的位置。
- **flags**：文件狀態標誌，使用八進制或十六進制表示。

    常見的文件狀態標誌及其值：

    | 標誌        | 十六進制值 | 八進制值 | 說明               |
    |------------|------------|----------|--------------------|
    | `O_RDONLY` | `0x0000`   | `0000000`| 只讀模式           |
    | `O_WRONLY` | `0x0001`   | `0000001`| 只寫模式           |
    | `O_RDWR`   | `0x0002`   | `0000002`| 讀寫模式           |
    | `O_APPEND` | `0x0400`   | `0002000`| 追加模式           |
    | `O_NONBLOCK` | `0x0800` | `0004000`| 非阻塞模式         |
    | `O_CREAT`  | `0x0100`   | `0001000`| 如果文件不存在則創建 |
    | `O_TRUNC`  | `0x0200`   | `0002000`| 打開文件時截斷其內容 |
    | `O_EXCL`   | `0x0800`   | `0004000`| 和 `O_CREAT` 一起使用，文件已存在則失敗 |

- **mnt_id**：掛載點 ID，是一個唯一標識文件系統掛載點的 ID。
- **ino**：`inode` 號，是文件在文件系統中的唯一標識號。

<!-- ### 總結

通過上述步驟和詳細解釋，你可以理解 `inode`、`inode table`、`file descriptor` 和 `file table` 的定義與關係，並掌握如何使用 GDB 和 `lsof` 等工具來調試程序，檢查文件描述符的狀態。 -->
