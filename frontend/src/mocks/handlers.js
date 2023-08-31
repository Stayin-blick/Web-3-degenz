import { rest } from "msw";

const baseURL = "https://web-3-degenz-f7ab1c03f599.herokuapp.com/";

export const handlers = [
  rest.get(`${baseURL}dj-rest-auth/user/`, (req, res, ctx) => {
    return res(
      ctx.json({
        "pk": 1,
        "username": "admin1",
        "email": "",
        "first_name": "",
        "last_name": "",
        "profile_id": 1,
        "profile_image": "https://res.cloudinary.com/daxaksdnm/image/upload/v1/media/../default_profile_sm6cnd"
      })
    );
  }),
  rest.post(`${baseURL}dj-rest-auth/logout/`, (req, res, ctx) => {
    return res(ctx.status(200));
  }),
];

