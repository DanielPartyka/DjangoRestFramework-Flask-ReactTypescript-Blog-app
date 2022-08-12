export interface PostsI {
    id: number;
    topic: string;
    text: string;
    user_id: number;
    tags: [];
    nick: string;
    likes: number;
    dislikes: number;
    children: JSX.Element[];
}