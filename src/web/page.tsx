import Image from 'next/image'
import Navbar from './navbar'; 
import fotobareng from './PhotoBareng.jpg'
import Son from './fotoson.jpg'
import Github from './Github.png'
import Instagram from './Instagram.png'
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
        <div className="Page bg-[#83C5BE] w-[100%] h-[100vh] overflow-x-hidden">
        <Navbar /> 
          <div className="Top flex justify-center mb-[100px] mt-[20px]">
          <div className="Information-Block w-[90%] h-[500px] bg-[#FFDDD2] mt-[50px] rounded-[40px] flex justify-center ">
          <Image
            src={fotobareng}
            alt='FotoBareng'
            className=' rounded-[40px] mx-[30px] my-[30px]'
            width={400}  // Replace with actual width
            height={100} // Replace with actual height
          />
          <div className="Text font-Merriweather  mt-[50px] mr-[60px]">
            <h1 className='text-[#006D77] text-[40px] text-center font-black'>Kosu Salted Caramel</h1>
            <p className='text-[#006D77] text-[20px] text-justify font-semibold mt-[30px]'>Three highly motivated and enthusiastic informatics students from the prestigious Bandung Institute of Technology, with a deep-seated passion and immense curiosity for the expansive and ever-evolving field of informatics, embarked on an ambitious mini project. Driven by an insatiable thirst for knowledge and a desire to apply theoretical concepts in a practical environment, they meticulously crafted a state-of-the-art Content-Based Image Retrieval (CBIR) web application. This project was not just a simple academic exercise; it was a journey into the depths of technological innovation and application.</p>
          </div>
          </div>
          </div>
          <div className="Card-Page w-[100%] bg-[#FFDDD2] pt-[70px] pb-[200px] ">
          <h1 className='text-[#006D77] text-[40px] text-center font-black font-Merriweather my-[20px]'>Developers</h1>
          <div className="Cardoverall flex justify-evenly ">
            <div className="flex justify-evenly flex-wrap">
              <div className="Card1 group relative items-center justify-center overflow-hidden cursor-pointer rounded-[20px] mx-[50px] my-[30px] border-[#E29578] border-[30px]">
                <div className="h-96 w-64 ">
                  <Image
              src={Son}
              alt='son'
              className='object-cover group-hover:rotate-3 group-hover:scale-125 transition-transform'
              layout='fill'
            />
                </div>
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/50 via-transparent to-black group-hover:from-black/70 group-hover: via-black/60 group-hover:to-black/70"></div>
                <div className="absolute inset-[-30px] flex flex-col items-center justify-center px-9 text-center translate-y-[60%] group-hover:translate-y-0 transition-all font-Merriweather">
                  <h1 className='text-2xl font-bold text-[#B2F7EF]'>Raden Rafly Hanggaraksa B</h1>
                  <p className='text-lg italic text-[#B2F7EF] mb-3'>13522014</p>
                  <div className="Social-Media flex justify center">
                    <a href="https://github.com/raflyhangga" target="_blank">
                    <Image
                      src={Github}
                      alt='Github'
                      className=' rounded-[40px] mx-[10px]'
                      width={50}  // Replace with actual width
                      height={50} // Replace with actual height
                    />
                    </a>
                    <a href="https://instagram.com/raflyhangga?igshid=OGQ5ZDc2ODk2ZA==" target="_blank">
                    <Image
                      src={Instagram}
                      alt='Instagram'
                      className=' rounded-[40px] mx-[10px]'
                      width={50}  // Replace with actual width
                      height={50} // Replace with actual height
                    />
                    </a>
                  </div>
                </div>
              </div>
              <div className="Card2 rounded-[20px] group relative items-center justify-center overflow-hidden cursor-pointer mx-[50px] my-[30px] border-[#E29578] border-[30px]">
                <div className="h-96 w-64">
                  <Image
              src={Son}
              alt='son'
              className='object-cover group-hover:rotate-3 group-hover:scale-125 transition-transform'
              layout='fill'
            />
                </div>
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/50 via-transparent to-black group-hover:from-black/70 group-hover: via-black/60 group-hover:to-black/70"></div>
                <div className="absolute inset-[-20px] flex flex-col items-center justify-center px-9 text-center translate-y-[60%] group-hover:translate-y-0 transition-all font-Merriweather ">
                  <h1 className='text-2xl font-bold text-[#B2F7EF]'>Wilson Yusda</h1>
                  <p className='text-lg italic text-[#B2F7EF] mb-3'>13522019</p>
                  <div className="Social-Media flex justify center">
                    <a href="https://github.com/Razark-Y" target="_blank">
                    <Image
                      src={Github}
                      alt='Github'
                      className=' rounded-[40px] mx-[10px] '
                      width={50}  // Replace with actual width
                      height={50} // Replace with actual height
                    />
                    </a>
                    <a href="https://instagram.com/wilson_yusda?igshid=OGQ5ZDc2ODk2ZA==" target="_blank">
                    <Image
                      src={Instagram}
                      alt='Instagram'
                      className=' rounded-[40px] mx-[10px] '
                      width={50}  // Replace with actual width
                      height={50} // Replace with actual height
                    />
                    </a>
                  </div>
                </div>
              </div>
              <div className="Card3 rounded-[20px] group relative items-center justify-center overflow-hidden cursor-pointer  mx-[50px] my-[30px] border-[#E29578] border-[30px]">
                <div className="h-96 w-64">
                  <Image
              src={Son}
              alt='son'
              className='object-cover group-hover:rotate-3 group-hover:scale-125 transition-transform '
              layout='fill'
            />
                </div>
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/50 via-transparent to-black group-hover:from-black/70 group-hover: via-black/60 group-hover:to-black/70"></div>
                <div className="absolute inset-[-30px] flex flex-col items-center justify-center px-9 text-center translate-y-[60%] group-hover:translate-y-0 transition-all font-Merriweather">
                  <h1 className='text-2xl font-bold text-[#B2F7EF]'>Abdul Rafi Radityo Hutomo</h1>
                  <p className='text-lg italic text-[#B2F7EF] mb-3'>13522089</p>
                  <div className="Social-Media flex justify center">
                    <a href="https://github.com/abdulrafirh" target="_blank">
                    <Image
                      src={Github}
                      alt='Github'
                      className=' rounded-[40px] mx-[10px] '
                      width={50}  // Replace with actual width
                      height={50} // Replace with actual height
                    />
                    </a>
                    <a href="https://instagram.com/abdulrafirh?igshid=OGQ5ZDc2ODk2ZA==" target="_blank">
                    <Image
                      src={Instagram}
                      alt='Instagram'
                      className=' rounded-[40px] mx-[10px] '
                      width={50}  // Replace with actual width
                      height={50} // Replace with actual height
                    />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          </div>
        </div>  
    </main>
  );
}