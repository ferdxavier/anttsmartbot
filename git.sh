DESC="Update"
git add .
git commit -m "$DESC"
git push origin $1
echo "Branch $1 pushed sucessfully"
