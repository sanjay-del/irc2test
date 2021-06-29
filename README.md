# irc2test

To run the entire tests from the tests/ move out of the irc2test directory and run
  
    $ tbears test basicirc2

If you wish to run a particular test method then run 
   
    $ python -m unittest basicirc2.tests.<<test_file_name>>.<<test_class_name>>.<<method>>
    
For example, to run total supply test from unit test   
    
    $ python -m unittest basicirc2.tests.test_unit_basicir2.TestSimple.test_total_supply
