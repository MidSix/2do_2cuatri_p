USER_HOME="/home/ubuntu" 

echo "Removing previous keys"
rm -f ${USER_HOME}/.ssh/id_ed25519
rm -f ${USER_HOME}/.ssh/id_ed25519.pub

echo "Deploying the private part of the key"
mkdir -p ${USER_HOME}/.ssh
echo "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBxn9uzxZrvZm6oKTveEnTq/Y3nRnS9TUeK0+ujCGJRMwAAAJCQNV9ekDVf
XgAAAAtzc2gtZWQyNTUxOQAAACBxn9uzxZrvZm6oKTveEnTq/Y3nRnS9TUeK0+ujCGJRMw
AAAEC/j5ZKn/Evz0JT/i8ZzL7uXI/uNEjPlI5E5GqiNvZUvnGf27PFmu9mbqgpO94SdOr9
jedGdL1NR4rT66MIYlEzAAAAB3Jvb3RATVIBAgMEBQY=
-----END OPENSSH PRIVATE KEY-----" >> ${USER_HOME}/.ssh/id_ed25519
chmod 400 ${USER_HOME}/.ssh/id_ed25519

echo "Deploying the public part of the key"
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHGf27PFmu9mbqgpO94SdOr9jedGdL1NR4rT66MIYlEz alumno@ParalelismoCD" >> ${USER_HOME}/.ssh/id_ed25519.pub

