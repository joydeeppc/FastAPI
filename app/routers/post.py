from fastapi import FastAPI,Response,status,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..import models, schemas,oauth2
from ..database import  get_db
from typing import List,Optional

## this is the router object
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]        ## this is used to group user and post routers saperetely in fastapi documentation             

)               


## to get all posts
# @router.get("/",response_model=List[schemas.Post])     
@router.get("/",response_model=List[schemas.PostOut])                                      
def get_posts(db: Session = Depends(get_db),current_user : int =  Depends(oauth2.get_current_user), limit:int =10, skip : int =0, search: Optional[str]= " "):              ## anytime you want to work with the database,remember, you have to pass it in to the path operation function. So this is going to make it a dependency.
    
    # cursor.execute("""SELECT * FROM posts """)  
    # posts = cursor.fetchall()
    print(limit)
    print(search)

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    ##We will join 2 tables. And by default with sql alchemy its left inner join. We need left Outer join.
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    ## The below command is used to get the post of the user who is logged in . Not posts of all users
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # print(posts)
    return  posts
   


@router.get("/{id}",response_model=schemas.PostOut)    
def get_post(id : int,db: Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id =  %s """, (str(id)))
    # post=cursor.fetchone()    #this will return something
    # print(test_post)
    # post = find_posts(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()           ## here we are using first() instead of all() is because if we use all then it will check all the id even if u got the required one
    # print(post)
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first() 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    ## The below logic is only to get the post of the user who logged in with a specific Id.
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the required action ")
    
        
    
    return  post    



@router.post("/", status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):   
    
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s ) RETURNING *""", (post.title, post.content,post.published))        # Here %s is a variable. Its actually sanatazing this code. Protecting us from sql injection attack.
    # new_post = cursor.fetchone()
    # conn.commit()       ## This is to save it in the database
    # new_post= models.Post(title=post.title,content= post.content,published=post.published)
    # print(**post.dict())
    
    # print(current_user.email)
    

    ## "owner_id=current_user.id" is the foreign key. This means that the id will be the id of the user who logged in to the system
    new_post= models.Post(owner_id=current_user.id,**post.dict())         ## **post.dict() is unpacking the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)         ## its doing the same thing as the RETURNING * so in sql
    return new_post  
     

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db),current_user : int =  Depends(oauth2.get_current_user)):
    

    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()   #to fetch the deleted post
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    ## The below logic is to make sure that the user is only deleting his post not someone else posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the required action ")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)      ## this is special for deleting a post. need to return response for this

@router.put("/{id}",response_model=schemas.Post)
def update_posts(id : int, updated_post : schemas.PostCreate,db: Session = Depends(get_db),current_user : int =  Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title= %s, content = %s,published = %s WHERE id = %s RETURNING *""", (post.title,post.content,post.published, str(id)))
    
    # updated_post = cursor.fetchone() #to fetch the updated post
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    ## The below logic is to make sure that the user is only updating his post not someone else posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the required action ")
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    return  post_query.first()