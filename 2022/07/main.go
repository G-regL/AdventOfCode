package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

type File struct {
	Name string
	Size int
}

type Folder struct {
	Name    string
	Files   []File
	Folders map[string]*Folder
	Size    int
}

func newFolder(name string) *Folder {
	return &Folder{name, []File{}, make(map[string]*Folder), 0}
}

func (f *Folder) getFolder(name string) *Folder {
	if nextF, ok := f.Folders[name]; ok {
		return nextF
	} else {
		//log.Fatalf("Expected nested folder %v in %v\n", name, f.Name)
		return nil
	}
	return &Folder{} // cannot happen
}

func (f *Folder) addFolder(path []string) {
	for i, segment := range path {
		if i == len(path)-1 { // last segment == new folder
			f.Folders[segment] = newFolder(segment)
		} else {
			f.getFolder(segment).addFolder(path[1:])
		}
	}
}

func (f *Folder) addFile(path []string, size int) {
	for i, segment := range path {
		if i == len(path)-1 { // last segment == file
			f.Files = append(f.Files, File{segment, size})
		} else {
			f.getFolder(segment).addFile(path[1:], size)
			return
		}
	}
}

func (f *Folder) String() string {
	var str string
	for _, file := range f.Files {
		str += f.Name + string(filepath.Separator) + file.Name + "\n"
	}
	for _, folder := range f.Folders {
		str += folder.String()
	}
	return str
}

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func main() {

	flag.Parse()
	filename := "input.txt"

	// Detect the --test flag and use test data if needed
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	// Open file for reading
	f, _ := os.Open(filename)
	defer f.Close()

	scanner := bufio.NewScanner(f)

	structure := map[string]int{}
	currentWorkingDir := []string{}
	for scanner.Scan() {
		line := string(scanner.Text())

		if strings.HasPrefix(line, "$ cd") {
			// command (cd/ls)
			//$ cd /
			newdir := ""
			_, _ = fmt.Sscanf(line, "$ cd %s", &newdir)

			if newdir == ".." {
				currentWorkingDir = currentWorkingDir[:len(currentWorkingDir)-1]
			} else {
				currentWorkingDir = append(currentWorkingDir, newdir)
			}
			//fmt.Println("changed CWD to ", currentWorkingDir)

		} else {
			//listing
			if strings.HasPrefix(line, "dir") {
				dir := ""
				_, _ = fmt.Sscanf(line, "dir %s", &dir)

				dirpath := strings.Join(append(currentWorkingDir, dir), "/")

				if _, ok := structure[dirpath]; !ok {
					//fmt.Println("folder", dirpath, "doesn't exist")
					structure[dirpath] = 0
				}
			} else {
				size := 0
				file := ""
				_, _ = fmt.Sscanf(line, "%d %s", &size, &file)

				//filepath := strings.Join(append(currentWorkingDir, file), "/")
				//structure[filepath] = size
				for i := len(currentWorkingDir); i != 0; i-- {
					structure[strings.Join(currentWorkingDir[:i], "/")] += size
				}

			}
		}
		//fmt.Println("CWD: ", currentWorkingDir)
	}

	sumP1 := 0
	for _, v := range structure {
		//fmt.Println(k, v)
		if v <= 100000 {
			sumP1 += v
		}
	}

	fmt.Println("Part 1 sum:", sumP1)
	//fmt.Println("Free Space:", 70000000-structure["/"])
	//fmt.Println("Needed Space:", 30000000-(70000000-structure["/"]))

	delete := 30000000
	for _, v := range structure {
		//fmt.Println(k, v)
		if v >= 30000000-(70000000-structure["/"]) && v <= delete {
			delete = v
		}
	}
	fmt.Println("Part 2 directory size:", delete)

}
