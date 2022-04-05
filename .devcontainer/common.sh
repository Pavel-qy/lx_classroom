USERNAME="somebody"

# # If in automatic mode, determine if a user already exists, if not use vscode
# if [ "${USERNAME}" = "auto" ] || [ "${USERNAME}" = "automatic" ]; then
#     USERNAME=""
#     POSSIBLE_USERS=("vscode" "node" "codespace" "$(awk -v val=1000 -F ":" '$3==val{print $1}' /etc/passwd)")
#     for CURRENT_USER in ${POSSIBLE_USERS[@]}; do
#         if id -u ${CURRENT_USER} > /dev/null 2>&1; then
#             USERNAME=${CURRENT_USER}
#             break
#         fi
#     done
#     if [ "${USERNAME}" = "" ]; then
#         USERNAME=vscode
#     fi
# elif [ "${USERNAME}" = "none" ]; then
#     USERNAME=root
#     USER_UID=0
#     USER_GID=0
# fi

# ** Shell customization section **
if [ "${USERNAME}" = "root" ]; then 
    user_rc_path="/root"
else
    user_rc_path="/home/${USERNAME}"
fi

# Codespaces bash and OMZ themes - partly inspired by https://github.com/ohmyzsh/ohmyzsh/blob/master/themes/robbyrussell.zsh-theme
codespaces_bash="$(cat \
<<'EOF'
# Codespaces bash prompt theme
__bash_prompt() {
    local userpart='`export XIT=$? \
        && [ ! -z "${GITHUB_USER}" ] && echo -n "\[\033[0;32m\]@${GITHUB_USER} " || echo -n "\[\033[0;32m\]\u " \
        && [ "$XIT" -ne "0" ] && echo -n "\[\033[1;31m\]➜" || echo -n "\[\033[0m\]➜"`'
    local gitbranch='`\
        export BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null); \
        if [ "${BRANCH}" != "" ]; then \
            echo -n "\[\033[0;36m\](\[\033[1;31m\]${BRANCH}" \
            && if git ls-files --error-unmatch -m --directory --no-empty-directory -o --exclude-standard ":/*" > /dev/null 2>&1; then \
                    echo -n " \[\033[1;33m\]✗"; \
               fi \
            && echo -n "\[\033[0;36m\]) "; \
        fi`'
    local lightblue='\[\033[1;34m\]'
    local removecolor='\[\033[0m\]'
    PS1="${userpart} ${lightblue}\w ${gitbranch}${removecolor}\n\$ "
    unset -f __bash_prompt
}
__bash_prompt
EOF
)"

# Add custom bash prompt
echo "${codespaces_bash}" >> "${user_rc_path}/.bashrc"
echo 'export PROMPT_DIRTRIM=4' >> "${user_rc_path}/.bashrc"

# Add custom bash prompt for root user (permission problems)
# if [ "${USERNAME}" != "root" ]; then
#     echo "${codespaces_bash}" >> "/root/.bashrc"
#     echo 'export PROMPT_DIRTRIM=4' >> "/root/.bashrc"
# fi
# chown ${USERNAME}:${USERNAME} "${user_rc_path}/.bashrc"
