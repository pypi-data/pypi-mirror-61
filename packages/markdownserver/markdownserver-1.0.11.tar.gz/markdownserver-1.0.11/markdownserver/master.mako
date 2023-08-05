<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Markdownserver</title>
    <link 
	  rel="stylesheet" 
	  href="/static/style.css">
    <link 
	  rel="stylesheet" 
	  href="/static/bootstrap.min.css">
  </head>
  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">Markdownserver</a>
    </nav>
    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-3 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
    		  ${toc}
            </ul>
    	  </div>
    	</nav>
    	 <main role="main" class="col-md-9 ml-sm-auto col-lg-9 px-4">
    	   ${content}
    	 </main>
      </div>
    </div>
  </body>
</html>
