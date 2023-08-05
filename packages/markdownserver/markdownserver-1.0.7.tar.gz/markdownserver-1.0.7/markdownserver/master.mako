<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Markdownserver</title>
    <link 
	  rel="stylesheet" 
	  href="/static/bootstrap.min.css">
    <style>
      .nav {
	    padding-top: 2em; 
	  }

      .nav ul {
	    padding-left: 1em;
	  }

      .nav li {
	    list-style: none;
	  }

	  .sidebar-sticky{
	    height: 100vh;
	  }
    </style>
  </head>
  <body>
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
