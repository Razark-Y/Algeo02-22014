import Image from 'next/image'
import Navbar from './navbar'; 
import RotomLogo from './RotomLogo.png';
import Bintang from './Bintang.svg';
export default function Home() {
  // const observer = new IntersectionObserver((entries) => {
  //   entries.forEach((entry)=>{
  //     console.log(entry)
  //     if(entry.isIntersecting){
  //       entry.target.classList.add('show');
  //     }
  //     else{
  //       entry.target.classList.remove('show');
  //     }
  //   })
  // })
  // const hiddenElements = document.querySelectorAll('.hidden');
  // hiddenElements.forEach((el)=>observer.observe(el));
  return (
    <main > 
        <div className="Page bg-[#83C5BE] w-[100%] h-[100vh] overflow-hidden">
          <div className="SideBox w-[31%] h-[100vh] bg-[#FFDDD2] absolute right-0 ">
          <Image
            src={RotomLogo}
            alt='RotomLogo'
            className='absolute right-[10px] top-[110px]'
            width={500}  // Replace with actual width
            height={300} // Replace with actual height
          />
          </div>
          <Navbar /> 
          <div className="Container pt-[220px] pl-[50px] text-[#006D77] absolute">
            <h1  className=" font-Merriweather font-black break-word w-[600px]  text-[54px]" >Reverse Image Search For Digital Users</h1>
            <h2  className=" font-Merriweather font-semibold break-word w-[500px]  text-[25px] font-" >A project done by Kosu Salted Caramel, Bandung Institute of Technology.</h2>
            <Image
            src={Bintang}
            alt='Bintang'
            className='absolute left-[450px]  top-[315px]'
            width={50}  // Replace with actual width
            height={30} // Replace with actual height
          />
          </div>
        </div>
    </main>
  );
}