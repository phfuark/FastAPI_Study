import BgHome from "../media/Banner_img.png";

import BreadIcon from "../assets/bread.svg"

export default function Home() {
  return (
    <div>
      <div className="w-full h-[67.5rem] bg-cover bg-center bg-no-repeat" style={{ backgroundImage: `url(${BgHome})` }}>
        <div className="flex text-3xl text-white">
            <div>
                <img src={BreadIcon} alt="" className="w-24 h-24 text-white"/>
            </div>
            <div>
                <p>Home</p>
                <p>Crete Employee</p>
                <p>Crete Product</p>
                <p>Crete Card</p>
            </div>
        </div>
      </div>
    </div>
  );
}
