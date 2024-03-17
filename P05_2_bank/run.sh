echo "Compiling..."
slice2py Bank.ice
slice2cpp Bank.ice
echo "Done!"
echo ""
echo "Running makefile..."
make
echo "Done!"
