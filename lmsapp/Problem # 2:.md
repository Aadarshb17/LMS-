Problem # 1:
Done--Write a query to display the book code, publication, price of the book witch is taken frequently.
##  Book.objects.values('isbn_number','publication',price)

Problem # 2:
Done--Write a query to display the member id, member name who have taken the book with book code ‘BL000002’.
## Student.objects.filter(issuedbook__book_id__isbn_number=109).values('user_id','user_id__first_name')

Done--Write a query to display the book code, book title and author of the books whose author name begins with ‘P’.
## Book.objects.filter(author_id__name__startswith='a').values('isbn_number', 'name', 'author_id__name')

Write a query to display the total number of Java books available in library with alias name ‘NO_OF_BOOKS’.
## Book.objects.filter(name='JAVA').values('quantity')

Write a query to list the category and number of books in each category with alias name ‘NO_OF_BOOKS’.
## a=Book.objects.values('category_id__category').annotate(entries=Count('name'))

Done--Write a query to display the number of books published by “Prentice Hall” with the alias name “NO_OF_BOOKS”.
## Book.objects.values('publication').annotate(entries=Count('publication')).filter(publication='Delhi')

Write a query to display the book code, book title of the books which are issued on the date “1st April 2012″.
## Book.objects.filter(issuedbook__issue_date='2022-10-20').values('isbn_number','name')
write a query to display the member id, member name, date of registration, membership status of the members who registered before “March 2012” 
## Student.objects.filter(user_id__date_joined__lte='2022-10-20').values('user_id__username', 'user_id', 'user_id__date_joined')

Write a query to display the average price of books which is belonging to ‘JAVA’ category with alias name “AVERAGEPRICE”.
## Book.objects.filter(name='JAVA').aggregate(Avg('price'))

Write a query to display the member id, member name, city and member status of members with the total fine paid by them with alias name “Fine”.
## Fine.objects.values('issue_id__roll_no__user_id','issue_id__roll_no__user_id__first_name', 'fine_amount')

Write a query to display the member id, member name of the members, book code and book title of the books taken by them.
## IssuedBook.objects.values('roll_no__user_id', 'roll_no__user_id__first_name','roll_no__user_id__last_name','book_id__isbn_number','book_id__name')

Write a query to display the total number of books available in the library with alias name “NO_OF_BOOKS_AVAILABLE” (Which is not issued).

Write a query to display the member id, member name, fine range and fine amount of the members whose fine amount is less than 100.
## Fine.objects.values('issue_id__roll_no__user_id','issue_id__roll_no__user_id__first_name', 'fine_amount').filter(fine_amount__lte='100')

Write a query to display the book code, book title, publisher, edition, price and year of publication and sort based on year of publication, publisher and edition.

Write a query to display the member id, member name, due date and date returned of the members who has returned the books after the due date. 

Write a query to display the member id, member name and date of registration who have not taken any book.

Write a Query to display the member id and member name of the members who has not paid any fine in the year 2012.
## Fine.objects.filter(fine_date='2022-10-20').values('issue_id__roll_no__user_id', 'issue_id__roll_no__user_id__first_name')


Write a query to display the date on which the maximum numbers of books were issued and the number of books issued with alias name “NOOFBOOKS”.
## IssuedBook.objects.values('issue_date').aggregate(Max('issue_date'))
 

Write a query to display book issue number, member name, date or registration, date of expiry, book title, category author, price, date of issue, date of return, actual returned date, fine amount.
## Fine.objects.values('issue_id', 'issue_id__roll_no__user_id__first_name', 'issue_id__roll_no__user_id__date_joined', 'issue_id__expiry_date', 'issue_id__book_id__name', 'issue_id__book_id__category_id__category', 'issue_id__issue_date', 'fine_date', 'fine_amount')


Write a query to display the book code, title, publish date of the books which is been published in the month of
December.
## Book.objects.filter(publication__istartswith='m').values('isbn_number','name','publication')


Write a query to display the member id, member name who have not returned the books.

