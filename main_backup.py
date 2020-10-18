import backup_github
import backup_gist

user='abarhub'

print("backup github")
rep_dest = "D:/backup/repo_github2/"
#rep_dest = "D:/temp/test_git2/"
#rep_dest = "D:/temp/test_git3/"
backup_github.backup_github(rep_dest, user)

print("backup gist")
backup_gist.backup_gist(rep_dest, user)
